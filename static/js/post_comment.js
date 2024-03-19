const comment = document.getElementById("comment");
const postId = document.getElementById("post_id").value;
const commentContainer = document.getElementById("comment-container");
const loadMoreComments = document.getElementById("load-more");
const noComments = document.getElementById("no-comments");
let comments = document.getElementById("comments");
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
        commentContainer.innerHTML += comment_template(comment);
      });
    });
}

function comment_template(comment) {
  let commentDate =
    comment.date_humanized === undefined ? "Now" : comment.date_humanized;
  let verified = "";

  if (comment.verified) {
    verified = `<i class="bi bi-patch-check ps-1" style="color: #b93be8"></i>`;
  }

  let commentElement = `
  <div class="comment mt-5">
    <div class="mt-3" style="display: flex; gap: 5px">
    <a href="/profile/${comment.user_id}/" class="link-dark text-decoration-none">
      <div style="
            display: inline-flex;
            justify-content: center;
            align-items: center;
          ">
        <img src="https://i.pravatar.cc/25" alt="User" class="img-fluid" style="border-radius: 50%; margin-right: 8px"
          width="25 px" />${comment.username} ${verified}
      </div>
    </a><i class="text-muted">says:</i>
    <span class="text-muted" style="margin-left: auto">
      <small><i class="me-1">${commentDate}</i>
      <a
            href="#"
            data-bs-toggle="dropdown"
            role="button"
            aria-expanded="false"
            ><i class="bi bi-three-dots-vertical" style="color: #bbb"></i
          ></a>
          <ul
            class="dropdown-menu"
            style="box-shadow: 0 0 10px rgba(0, 0, 0, 0.1)"
          >
            <li>
              <a class="dropdown-item" href="#">Answer Comment</a>
            </li>
        `;
  if (comment.user_id === currentUser) {
    commentElement += `
          <li><hr class="dropdown-divider" /></li>
            <li>
              <a
                href="/post/${postId}/comment/${comment.id}/delete/"
                class="link-danger dropdown-item"
                >Delete</a
              >
            </li>
          `;
  } else {
    commentElement += `
            <li><hr class="dropdown-divider" /></li>
            <li>
              <a class="link-danger dropdown-item" href="#">Report Comment</a>
            </li>`;
  }
  commentElement += `
          </ul>
          </small></span>
        </div>
        <div class="comment-content">${comment.content}</div>
      </div>
    <hr class="border border-1" />`;
  return commentElement;
}

function populateComments() {
  fetch(`/api/post/${postId}/get_last_posted_comment`)
    .then(response => response.json())
    .then(comment => {
      const commentElement = document.createElement("div");
      comment.username = currentUserName;
      comment.verified = currentUserVerified;
      commentElement.classList.add("newly-added-comment");
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
            comments.innerText = parseInt(comments.innerText) + 1;
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

// TODO: fix this, it's not working with javascript loaded comments
document.querySelectorAll(".link-danger").forEach(link => {
  link.addEventListener("click", e => {
    if (!confirm("Are you sure you want to delete this comment?")) {
      e.preventDefault();
    }
  });
});
