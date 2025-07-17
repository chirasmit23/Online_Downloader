
document.getElementById("option")?.addEventListener("change", (e) => {
  const selectedId = e.target.options[e.target.selectedIndex]?.id;
  const colorMap = {
    black: "black",
    blue: "blue",
  };
  document.body.style.transition = "none";
  document.body.style.backgroundColor = colorMap[selectedId] || "#082567";
});
function togglePassword() {
  const passwordInput = document.getElementById("password");
  const toggleIcon = document.getElementById("icon");
  if (!passwordInput || !toggleIcon) return;
  const isHidden = passwordInput.type === "password";
  passwordInput.type = isHidden ? "text" : "password";
  toggleIcon.textContent = isHidden ? "🙈" : "👁️";
}
function handleFormSubmit(form, endpoint, filenameTemplate) {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const button = form.querySelector(".download-button");
    const btnText = button?.querySelector(".btn-text");
    const spinner = button?.querySelector(".btn-spinner");
    button.disabled = true;
    if (btnText) btnText.style.display = "none";
    if (spinner) spinner.style.display = "inline-block";
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        body: new FormData(form),
      });
      const contentType = response.headers.get("Content-Type");
      if (response.status === 429) {
        try {
          const data = await response.json();
          showPopup(data.message || "Rate limit exceeded ❌", false);
        } catch {
          showPopup("Rate limit exceeded ❌", false);
        }
        throw new Error("Rate limited");
      }
      if (!response.ok) {
        try {
          const data = await response.json();
          showPopup(data.message || "Download failed ❌", false);
        } catch {
          showPopup("Download failed ❌", false);
        }
        throw new Error("Invalid response");
      }
      if (!contentType?.includes("video") && !contentType?.includes("image")) {
        showPopup("Invalid media type ❌", false);
        throw new Error("Invalid media");
      }
      const blob = await response.blob();
      const finalName = filenameTemplate.replace("{ts}", Date.now());
      const downloadLink = document.createElement("a");
      downloadLink.href = URL.createObjectURL(blob);
      downloadLink.download = finalName;
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
      showPopup("Download Successful ✅", true);
    } catch (err) {
      if (err.message !== "Rate limited") {
        showPopup("Download failed ❌", false);
      }
    } finally {
      button.disabled = false;
      if (btnText) btnText.style.display = "inline";
      if (spinner) spinner.style.display = "none";
      if (typeof overlay !== "undefined" && overlay) {
        overlay.style.display = "none";
      }
    }
  });
}
function handleFormSubmitIfExists(selector, endpoint, filenameTemplate) {
  const form = document.querySelector(selector);
  if (form) handleFormSubmit(form, endpoint, filenameTemplate);
}
function showPopup(message, isSuccess = true) {
  const popup = document.createElement("div");
  popup.className = "popup" + (isSuccess ? "" : " failed");
  popup.textContent = message;
  document.body.appendChild(popup);
  popup.style.display = "block";
  setTimeout(() => popup.remove(), 3000);
}
handleFormSubmitIfExists("#videoForm", "/video", "video_{ts}.mp4");
handleFormSubmitIfExists("#photoForm", "/photo", "photo_{ts}.jpg");
