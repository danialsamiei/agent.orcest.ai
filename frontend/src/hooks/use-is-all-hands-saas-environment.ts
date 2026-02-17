import { useMemo } from "react";

/**
 * Hook to check if the current domain is a Maestrist/Orcest SaaS environment
 * @returns True if the current domain contains "orcest.ai" or "maestrist.dev" postfix
 */
export const useIsAllHandsSaaSEnvironment = (): boolean =>
  useMemo(() => {
    const { hostname } = window.location;
    return (
      hostname.endsWith("orcest.ai") || hostname.endsWith("maestrist.dev")
    );
  }, []);
