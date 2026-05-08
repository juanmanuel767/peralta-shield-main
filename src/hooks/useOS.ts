import { useState, useEffect } from "react";

export type OS = "windows" | "macos" | "linux" | "unknown";

export function useOS() {
  const [os, setOS] = useState<OS>("unknown");

  useEffect(() => {
    const ua = window.navigator.userAgent.toLowerCase();
    if (ua.includes("win")) setOS("windows");
    else if (ua.includes("mac")) setOS("macos");
    else if (ua.includes("linux")) setOS("linux");
    else setOS("unknown");
  }, []);

  return os;
}
