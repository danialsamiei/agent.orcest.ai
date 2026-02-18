from typing import Any

from fastapi import HTTPException, status


class MaestristError(HTTPException):
    """General Error"""

    def __init__(
        self,
        detail: Any = None,
        headers: dict[str, str] | None = None,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class AuthError(MaestristError):
    """Error in authentication."""

    def __init__(
        self,
        detail: Any = None,
        headers: dict[str, str] | None = None,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class PermissionsError(MaestristError):
    """Error in permissions."""

    def __init__(
        self,
        detail: Any = None,
        headers: dict[str, str] | None = None,
        status_code: int = status.HTTP_403_FORBIDDEN,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class SandboxError(MaestristError):
    """Error in Sandbox."""
