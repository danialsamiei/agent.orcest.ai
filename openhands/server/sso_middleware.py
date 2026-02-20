"""
OAuth2/OIDC SSO middleware for Maestrist.
Enforces authentication via login.orcest.ai for all requests.

This module provides:
- SSOMiddleware: ASGI middleware that intercepts requests and validates SSO tokens
- sso_auth_router: FastAPI router with /auth/callback, /auth/logout, and /api/sso/me endpoints

Environment variables:
- SSO_ISSUER: Base URL of the OIDC issuer (default: https://login.orcest.ai)
- SSO_CLIENT_ID: OAuth2 client ID (default: maestrist)
- SSO_CLIENT_SECRET: OAuth2 client secret (required for code exchange)
- SSO_CALLBACK_URL: OAuth2 redirect URI (default: https://agent.orcest.ai/auth/callback)
"""

import logging
import os
import time
from typing import Any
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration from environment
# ---------------------------------------------------------------------------

SSO_ISSUER: str = os.getenv('SSO_ISSUER', 'https://login.orcest.ai')
SSO_CLIENT_ID: str = os.getenv('SSO_CLIENT_ID', 'maestrist')
SSO_CLIENT_SECRET: str = os.getenv('SSO_CLIENT_SECRET', '')
SSO_CALLBACK_URL: str = os.getenv(
    'SSO_CALLBACK_URL', 'https://agent.orcest.ai/auth/callback'
)

# Cookie name used to store the SSO access token
SSO_COOKIE_NAME = 'maestrist_sso_token'

# Token verification cache: maps token -> (verified_payload, expiry_timestamp)
_token_cache: dict[str, tuple[dict[str, Any], float]] = {}
_TOKEN_CACHE_TTL_SECONDS = 300  # 5 minutes

# ---------------------------------------------------------------------------
# Paths that do NOT require authentication
# ---------------------------------------------------------------------------

UNAUTHENTICATED_PATH_PREFIXES: tuple[str, ...] = (
    '/health',
    '/alive',
    '/auth/callback',
    '/auth/logout',
    '/api/litellm-models',
    '/api/options/models',
)

UNAUTHENTICATED_EXACT_PATHS: set[str] = {
    '/health',
    '/alive',
}


def _is_public_path(path: str) -> bool:
    """Return True if the path should be accessible without authentication."""
    if path in UNAUTHENTICATED_EXACT_PATHS:
        return True
    for prefix in UNAUTHENTICATED_PATH_PREFIXES:
        if path.startswith(prefix):
            return True
    return False


# ---------------------------------------------------------------------------
# Token verification
# ---------------------------------------------------------------------------


def _cache_cleanup() -> None:
    """Remove expired entries from the token cache."""
    now = time.monotonic()
    expired = [k for k, (_, exp) in _token_cache.items() if exp <= now]
    for k in expired:
        del _token_cache[k]


async def _verify_token(token: str) -> dict[str, Any] | None:
    """
    Verify an access token by calling the SSO issuer's token verification
    endpoint.  Returns the decoded user payload on success, or None on failure.

    Results are cached for up to 5 minutes.
    """
    _cache_cleanup()

    cached = _token_cache.get(token)
    if cached is not None:
        payload, expiry = cached
        if time.monotonic() < expiry:
            return payload

    verify_url = f'{SSO_ISSUER}/api/token/verify'
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                verify_url,
                json={'token': token},
                headers={'Content-Type': 'application/json'},
            )
        if resp.status_code == 200:
            payload = resp.json()
            _token_cache[token] = (payload, time.monotonic() + _TOKEN_CACHE_TTL_SECONDS)
            return payload
        else:
            logger.debug(
                'SSO token verification failed: status=%s body=%s',
                resp.status_code,
                resp.text[:200],
            )
            # Remove stale cache entry if token was previously valid
            _token_cache.pop(token, None)
            return None
    except httpx.HTTPError as exc:
        logger.warning('SSO token verification request failed: %s', exc)
        return None


def _extract_token(request: Request) -> str | None:
    """Extract the SSO token from the request cookie or Authorization header."""
    # 1. Try cookie first
    token = request.cookies.get(SSO_COOKIE_NAME)
    if token:
        return token

    # 2. Fall back to Bearer token in Authorization header
    auth_header = request.headers.get('authorization', '')
    if auth_header.lower().startswith('bearer '):
        return auth_header[7:].strip()

    return None


def _is_browser_request(request: Request) -> bool:
    """Heuristic: return True if the request likely comes from a web browser."""
    accept = request.headers.get('accept', '')
    return 'text/html' in accept


def _build_sso_login_url(redirect_after: str | None = None) -> str:
    """Build the SSO authorization URL to redirect unauthenticated browser users."""
    params = {
        'response_type': 'code',
        'client_id': SSO_CLIENT_ID,
        'redirect_uri': SSO_CALLBACK_URL,
        'scope': 'openid profile email',
    }
    if redirect_after:
        params['state'] = redirect_after
    return f'{SSO_ISSUER}/authorize?{urlencode(params)}'


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------


class SSOMiddleware(BaseHTTPMiddleware):
    """
    ASGI middleware that enforces SSO authentication on all routes except
    explicitly allowlisted paths.

    For authenticated requests, ``request.state.sso_user`` is populated with
    the verified user payload (containing at minimum ``sub``, ``name``,
    ``role``).

    Unauthenticated API requests receive a 401 JSON response.
    Unauthenticated browser requests are redirected to the SSO login page.
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        path = request.url.path

        # Allow public paths through without authentication
        if _is_public_path(path):
            return await call_next(request)

        token = _extract_token(request)
        if token is None:
            return self._unauthenticated_response(request)

        user_payload = await _verify_token(token)
        if user_payload is None:
            return self._unauthenticated_response(request)

        # Attach user info to request state so downstream handlers can use it
        request.state.sso_user = {
            'sub': user_payload.get('sub', ''),
            'name': user_payload.get('name', ''),
            'role': user_payload.get('role', ''),
            'email': user_payload.get('email', ''),
        }

        return await call_next(request)

    # ------------------------------------------------------------------

    @staticmethod
    def _unauthenticated_response(request: Request) -> Response:
        """Return a 401 JSON response or redirect depending on the client."""
        if _is_browser_request(request):
            login_url = _build_sso_login_url(redirect_after=str(request.url))
            return RedirectResponse(url=login_url, status_code=302)

        return JSONResponse(
            status_code=401,
            content={
                'error': 'authentication_required',
                'message': 'SSO authentication is required. Provide a valid token via '
                f'the "{SSO_COOKIE_NAME}" cookie or an Authorization: Bearer header.',
            },
        )


# ---------------------------------------------------------------------------
# Auth routes (FastAPI router)
# ---------------------------------------------------------------------------

sso_auth_router = APIRouter(tags=['SSO Authentication'])


@sso_auth_router.get('/auth/callback')
async def sso_callback(request: Request) -> Response:
    """
    OAuth2 authorization code callback.

    Exchanges the authorization code for tokens, sets the SSO cookie, and
    redirects the user to the application root (or to the URL stored in the
    ``state`` parameter).
    """
    code = request.query_params.get('code')
    state = request.query_params.get('state')  # optional redirect-after URL

    if not code:
        return JSONResponse(
            status_code=400,
            content={'error': 'missing_code', 'message': 'No authorization code provided.'},
        )

    # Exchange the code for tokens
    token_url = f'{SSO_ISSUER}/api/token'
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': SSO_CALLBACK_URL,
        'client_id': SSO_CLIENT_ID,
        'client_secret': SSO_CLIENT_SECRET,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                token_url,
                data=token_data,
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
            )
    except httpx.HTTPError as exc:
        logger.error('SSO token exchange request failed: %s', exc)
        return JSONResponse(
            status_code=502,
            content={'error': 'sso_unavailable', 'message': 'Unable to reach SSO server.'},
        )

    if resp.status_code != 200:
        logger.error(
            'SSO token exchange failed: status=%s body=%s',
            resp.status_code,
            resp.text[:300],
        )
        return JSONResponse(
            status_code=401,
            content={'error': 'token_exchange_failed', 'message': 'SSO token exchange failed.'},
        )

    token_response = resp.json()
    access_token = token_response.get('access_token', '')

    if not access_token:
        return JSONResponse(
            status_code=401,
            content={'error': 'no_access_token', 'message': 'No access token in SSO response.'},
        )

    # Determine redirect target
    redirect_url = state if state else '/'

    response = RedirectResponse(url=redirect_url, status_code=302)
    response.set_cookie(
        key=SSO_COOKIE_NAME,
        value=access_token,
        httponly=True,
        secure=True,
        samesite='lax',
        max_age=86400,  # 24 hours
        path='/',
    )
    return response


@sso_auth_router.get('/auth/logout')
async def sso_logout() -> Response:
    """
    Clear the SSO cookie and redirect the user to the SSO provider's logout
    endpoint so the session is terminated on both sides.
    """
    sso_logout_url = f'{SSO_ISSUER}/logout?redirect_uri={SSO_CALLBACK_URL}'

    response = RedirectResponse(url=sso_logout_url, status_code=302)
    response.delete_cookie(
        key=SSO_COOKIE_NAME,
        path='/',
        httponly=True,
        secure=True,
        samesite='lax',
    )
    return response


@sso_auth_router.get('/api/sso/me')
async def sso_me(request: Request) -> Response:
    """
    Return the current SSO user information.

    Requires a valid SSO token (cookie or Bearer header).
    If the SSO middleware is active, ``request.state.sso_user`` will be set.
    """
    sso_user = getattr(request.state, 'sso_user', None)
    if sso_user is None:
        return JSONResponse(
            status_code=401,
            content={'error': 'not_authenticated', 'message': 'No SSO session found.'},
        )

    return JSONResponse(status_code=200, content=sso_user)
