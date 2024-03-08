function updateSubmitButtonStatus() {
  const title = document.getElementById("title").value;
  const content = document.getElementById("content").value;
  const submitButton = document.getElementById("submit");

  const isEnabled = title.length > 0 && content.length > 0;
  submitButton.disabled = !isEnabled;
  submitButton.style.color = isEnabled ? "#444" : "grey";
}

document.getElementById("draft").addEventListener("change", function () {
  document.getElementById("submit").innerHTML = this.checked
    ? "Save Draft"
    : "Publish";
});

document.querySelectorAll("input, textarea").forEach(input => {
  input.addEventListener("input", () => {
    window.onbeforeunload = () => "You have unsaved changes!";
    updateSubmitButtonStatus();
  });
});

const form = document.querySelector("form");
form.addEventListener("submit", () => {
  window.onbeforeunload = null;
});

updateSubmitButtonStatus();
