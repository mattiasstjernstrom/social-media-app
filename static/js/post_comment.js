const comment = document.getElementById("comment");
const postId = document.getElementById("post_id").value;
const commentContainer = document.getElementById("comment-container");

function populateComments() {
  fetch(`/api/post/${postId}/get_last_posted_comment`)
    .then(response => response.json())
    .then(comment => {
      const commentElement = document.createElement("div");
      commentElement.classList.add("row", "p-3");
      commentElement.innerHTML = comment_template(comment);
      commentContainer.prepend(commentElement);
    });
}

if (comment) {
  comment.addEventListener("keypress", e => {
    if (e.key === "Enter") {
      e.preventDefault();
      const form = document.getElementById("comment-form");
      const formData = new FormData(form);
      let counter = 10;
      fetch(`/post/${postId}/comment/`, {
        method: "POST",
        body: formData,
      })
        .then(async response => {
          if (response.status === 201) {
            console.log("Comment posted.");
          } else {
            alert("Failed to post comment.");
          }
        })
        .then(() => {
          if (noComments) {
            noComments.style.display = "none";
          }
          populateComments();
          comment.value = "";
          // disable comments for a while
          comment.setAttribute("disabled", true);

          for (let i = 0; i < counter; i++) {
            setTimeout(() => {
              counter--;
              comment.setAttribute(
                "placeholder",
                `Commenting is disabled for ${counter} seconds.`
              );
            }, i * 1000);
          }
          setTimeout(() => {
            comment.removeAttribute("disabled");
            comment.value = "";
            comment.setAttribute("placeholder", "Do you have more to say?");
          }, counter * 1000);
          isThereMoreComments();
        })

        .catch(error => {
          console.error("Error:", error);
        });
    }
  });
} else {
  console.log("Comments is disabled.");
}
