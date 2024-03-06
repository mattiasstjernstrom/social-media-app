document.querySelectorAll(".link-danger").forEach(link => {
  link.addEventListener("click", e => {
    if (!confirm("Are you sure you want to delete this post?")) {
      e.preventDefault();
    }
  });
});
