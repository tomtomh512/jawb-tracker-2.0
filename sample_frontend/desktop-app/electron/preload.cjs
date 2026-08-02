const { contextBridge } = require("electron");

// The renderer (the same React app used by the website) talks to the FastAPI
// backend over plain HTTP via fetch(), so no privileged IPC bridge is required.
// This preload just exposes a small marker so the app can tell it's running
// inside the desktop shell if it ever wants to (e.g. hide a "download the app"
// banner).
contextBridge.exposeInMainWorld("jawbDesktop", {
  isDesktopApp: true,
  platform: process.platform,
});
