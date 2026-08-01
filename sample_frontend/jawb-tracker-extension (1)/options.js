async function init() {
  const settings = await getSettings();
  document.getElementById("apiBaseUrl").value = settings.apiBaseUrl;
  document.getElementById("webAppUrl").value = settings.webAppUrl;
}

document.getElementById("saveBtn").addEventListener("click", async () => {
  const apiBaseUrl = document.getElementById("apiBaseUrl").value.trim() || undefined;
  const webAppUrl = document.getElementById("webAppUrl").value.trim() || undefined;
  await setSettings({
    ...(apiBaseUrl ? { apiBaseUrl } : {}),
    ...(webAppUrl ? { webAppUrl } : {}),
  });
  const hint = document.getElementById("savedHint");
  hint.textContent = "Saved.";
  setTimeout(() => (hint.textContent = ""), 2000);
});

init();
