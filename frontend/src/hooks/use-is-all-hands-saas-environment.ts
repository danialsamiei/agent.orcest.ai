import { useMemo } from "react";

/**
 * Hook to check if the current domain is an All Hands SaaS environment
 * @returns True if the current domain contains "orcest.ai" or "orcest.ai" postfix
 */
export const useIsAllHandsSaaSEnvironment = (): boolean =>
  useMemo(() => {
    const { hostname } = window.location;
    return (
      hostname.endsWith("orcest.ai") || hostname.endsWith("orcest.ai")
    );
  }, []);
