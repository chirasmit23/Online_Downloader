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
function showPopup(message) {
  const popup = document.createElement("div");
  popup.className = "popup failed";
  popup.textContent = message;
  document.body.appendChild(popup);
  popup.style.display = "block";
  setTimeout(() => popup.remove(), 3000);
}
function FormSubmit(form, endpoint, filenameTemplate) {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const button = form.querySelector(".download-button");
    const btnText = button?.querySelector(".btn-text");
    const spinner = button?.querySelector(".btn-spinner");

    if (button) button.disabled = true;
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
          showPopup(data.message || "Rate limit exceeded ❌");
        } catch {
          showPopup("Rate limits exceeded ❌");
        }
        return;
      }
      if (!response.ok || !contentType?.includes("video") && !contentType?.includes("image")) {
        try {
          const data = await response.json();
          showPopup(data.message || "Download failed ❌");
        } catch {
          showPopup("Download failed ❌");
        }
        return;
      }
      const blob = await response.blob();
      const finalName = filenameTemplate.replace("{ts}", Date.now());
      const downloadLink = document.createElement("a");
      downloadLink.href = URL.createObjectURL(blob);
      downloadLink.download = finalName;
      document.body.appendChild(downloadLink);
      downloadLink.click();
      setTimeout(() => document.body.removeChild(downloadLink), 500);
    } catch (err) {
      showPopup("Unexpected error occurred ❌");
    } finally {
      if (button) button.disabled = false;
      if (btnText) btnText.style.display = "inline";
      if (spinner) spinner.style.display = "none";
    }
  });
}
function FormSubmitIfExists(selector, endpoint, filenameTemplate) {
  const form = document.querySelector(selector);
  if (form) FormSubmit(form, endpoint, filenameTemplate);
}
FormSubmitIfExists("#videoForm", "/video", "video_{ts}.mp4");
FormSubmitIfExists("#photoForm", "/photo", "photo_{ts}.jpg");
