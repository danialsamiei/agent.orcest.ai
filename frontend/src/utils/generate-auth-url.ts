/**
 * Generates a URL to redirect to for OAuth authentication
 * @param identityProvider The identity provider to use (e.g., "github", "gitlab", "bitbucket", "azure_devops")
 * @param requestUrl The URL of the request
 * @returns The URL to redirect to for OAuth
 */
export const generateAuthUrl = (
  identityProvider: string,
  requestUrl: URL,
  authUrl?: string | null,
) => {
  // Use HTTPS protocol unless the host is localhost
  const protocol =
    requestUrl.hostname === "localhost" ? requestUrl.protocol : "https:";
  const redirectUri = `${protocol}//${requestUrl.host}/oauth/keycloak/callback`;

  let finalAuthUrl: string;

  if (authUrl) {
    // Ensure https:// is prepended and remove any accidental duplicate slashes
    finalAuthUrl = `https://${authUrl.replace(/^https?:\/\//, "")}`;
  } else {
    finalAuthUrl = requestUrl.hostname
      .replace(/(^|\.)staging\.orcest\.ai$/, "$1auth.staging.orcest.ai")
      .replace(/(^|\.)agent\.orcest\.ai$/, "auth.agent.orcest.ai")
      .replace(/(^|\.)localhost$/, "auth.staging.orcest.ai");

    // If no replacements matched, prepend "auth." (excluding localhost)
    if (
      finalAuthUrl === requestUrl.hostname &&
      requestUrl.hostname !== "localhost"
    ) {
      finalAuthUrl = `auth.${requestUrl.hostname}`;
    }

    finalAuthUrl = `https://${finalAuthUrl}`;
  }

  const scope = "openid email profile"; // OAuth scope - not user-facing
  const separator = requestUrl.search ? "&" : "?";
  const cleanHref = requestUrl.href.replace(/\/$/, "");
  const state = `${cleanHref}${separator}login_method=${identityProvider}`;
  return `${finalAuthUrl}/realms/maestrist/protocol/openid-connect/auth?client_id=maestrist&kc_idp_hint=${identityProvider}&response_type=code&redirect_uri=${encodeURIComponent(redirectUri)}&scope=${encodeURIComponent(scope)}&state=${encodeURIComponent(state)}`;
};
