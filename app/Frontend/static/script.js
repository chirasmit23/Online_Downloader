document.getElementById("option")?.addEventListener("change", (e) => {
  const selectedId = e.target.options[e.target.selectedIndex]?.id;
  const colorMap = {
    black: "black",
    red: "red",
    green: "green",
    blue: "blue",
    yellow: "yellow"
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
    const btnText = button.querySelector(".btn-text");
    const spinner = button.querySelector(".btn-spinner");
    const layer = document.getElementById("downloadOverlay");
    button.disabled = true;
    btnText.style.display = "none";
    spinner.style.display = "inline-block";
    if (layer) layer.style.display = "flex";
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        body: new FormData(form)
      });
      if (response.status === 429) {
        const data = await response.json();
        showPopup(data.message || "Rate limit exceeded.", false);
        throw new Error("Rate limited");
      }
      if (!response.ok) {
        const data = await response.json();
        showPopup(data.message || "Download failed.", false);
        throw new Error("Download error");
      }
      const blob = await response.blob();
      const downloadLink = document.createElement("a");
      const finalName = filenameTemplate.replace("{ts}", Date.now());
      downloadLink.href = URL.createObjectURL(blob);
      downloadLink.download = finalName;
      document.body.appendChild(downloadLink);
      downloadLink.click();
      document.body.removeChild(downloadLink);
      showPopup("Download Successful ✅", true);
    } catch (err) {
      if (err.message !== "Rate limited") {
        showPopup("Download failed. Try again.", false);
      }
    } finally {
      button.disabled = false;
      btnText.style.display = "inline";
      spinner.style.display = "none";
      if (overlay) overlay.style.display = "none";
    }
  });
}
function handleFormSubmitIfExists(selector, endpoint, filenameTemplate) {
  const form = document.querySelector(selector);
  if (form) {
    handleFormSubmit(form, endpoint, filenameTemplate);
  }
}
handleFormSubmitIfExists("#videoForm", "/video", "video_{ts}.mp4");
handleFormSubmitIfExists("#photoForm", "/photo", "photo_{ts}.jpg");
