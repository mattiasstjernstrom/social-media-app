const comment = document.getElementById("comment");
const postId = document.getElementById("post_id").value;
const commentContainer = document.getElementById("comment-container");
const loadMoreComments = document.getElementById("load-more");
const noComments = document.getElementById("no-comments");
let offset = 10;
const limit = 10;
isThereMoreComments();
if (!noComments) {
  loadMoreComments.addEventListener("click", () => {
    fetchMoreComments();
  });
}

function isThereMoreComments() {
  fetch(`/api/post/${postId}/comments/?limit=${limit}&offset=${offset}`)
    .then(response => response.json())
    .then(data => {
      if (data.length !== 0) {
        loadMoreComments.classList.remove("d-none");
      }
    });
}

function fetchMoreComments() {
  fetch(`/api/post/${postId}/comments/?limit=${limit}&offset=${offset}`)
    .then(response => response.json())
    .then(data => {
      if (data.length === 0) {
        loadMoreComments.classList.add("d-none");
        return;
      }
      offset += 10;
      data.forEach(comment => {
        const commentElement = document.createElement("div");
        commentElement.classList.add("row", "p-3");
        commentElement.innerHTML = comment_template(comment);
        commentContainer.appendChild(commentElement);
      });
    });
}

function comment_template(comment) {
  let commentDate =
    comment.date_humanized === undefined ? "now" : comment.date_humanized;
  let commentElement = `
    <div class="col-1">
        <img
            src="https://via.placeholder.com/50"
            alt="User"
            class="img-fluid"
            style="border-radius: 50%" />
    </div>
    <div class="col">
        <div class="card">
            <div class="card-body">
                <strong class="card-title">
                    <a
                        href="/profile/${comment.user_id}/"
                        class="link-dark"
                        style="text-decoration: none"
                        >${comment.username}</a
                    >
                </strong>
                says:
                <p class="card-text">${comment.content}</p>
                <small>${commentDate}</small>`;
  if (comment.user_id === currentUser) {
    commentElement += ` &middot;
              <a
                href="/post/${postId}/comment/${comment.id}/delete/"
                class="link-danger"
                >Delete</a
              >`;
  }
  commentElement += `</small>
            </div>
        </div>
    </div>
    `;
  return commentElement;
}

function populateComments() {
  fetch(`/api/post/${postId}/get_last_posted_comment`)
    .then(response => response.json())
    .then(comment => {
      const commentElement = document.createElement("div");
      comment.username = currentUserName;
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
document.querySelectorAll(".link-danger").forEach(link => {
  link.addEventListener("click", e => {
    if (!confirm("Are you sure you want to delete this comment?")) {
      e.preventDefault();
    }
  });
});
