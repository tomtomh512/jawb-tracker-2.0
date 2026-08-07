import { useMemo } from "react";
import { makeApi } from "./client";
import { useSettings } from "../context/SettingsContext";

export function useApi() {
  const { settings } = useSettings();
  return useMemo(() => makeApi(settings.apiBaseUrl), [settings.apiBaseUrl]);
}
