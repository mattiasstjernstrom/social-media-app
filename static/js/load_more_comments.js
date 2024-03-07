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
  let fixedDate = formatCommentDate(comment.date_commented);
  return `
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
                        >${comment.user_id}</a
                    >
                </strong>
                says:
                <p class="card-text">${comment.content}</p>
                <small>${fixedDate}</small>
            </div>
        </div>
    </div>
    `;
}
