// Humanize time
function humanizeTime(dateString) {
  let dt = new Date(dateString);
  let now = new Date();
  let diff = now - dt;

  let seconds = Math.floor(diff / 1000);
  let minutes = Math.floor(seconds / 60);
  let hours = Math.floor(minutes / 60);
  let days = Math.floor(hours / 24);

  if (seconds < 60) {
    return "a moment ago";
  } else if (seconds < 3600) {
    return `${minutes} minutes ago`;
  } else if (seconds < 7200) {
    return "one hour ago";
  } else if (seconds < 86400) {
    return `${hours} hours ago`;
  } else if (seconds < 172800) {
    return "yesterday";
  } else if (days < 365) {
    let month = dt.toLocaleString("default", { month: "long" });
    let day = dt.getDate();
    return `${month} ${day}`;
  } else {
    let year = dt.getFullYear();
    let month = (dt.getMonth() + 1).toString().padStart(2, "0");
    let day = dt.getDate().toString().padStart(2, "0");
    return `${year}-${month}-${day}`;
  }
}

// Global date formatter function
function formatCommentDate(dateString) {
  let date = new Date(dateString);
  let year = date.getFullYear();
  let month = (date.getMonth() + 1).toString().padStart(2, "0");
  let day = date.getDate().toString().padStart(2, "0");
  let hours = date.getHours().toString().padStart(2, "0");
  let minutes = date.getMinutes().toString().padStart(2, "0");
  let seconds = date.getSeconds().toString().padStart(2, "0");

  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}
