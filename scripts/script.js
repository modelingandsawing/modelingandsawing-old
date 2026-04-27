function showNavigationMenu() {
  const target = document.querySelector("div#navigation-menu");
  if (target) {
    target.style.visibility = "visible";
  }
}

document.onclick = (e) => {
  // Hide the navigation menu
  if (e.target.id !== "icon-navigation-menu") {
    const target = document.querySelector("div#navigation-menu");
    if (target) {
      target.style.visibility = "hidden";
    }
  }
};

HTMLElement.prototype.switchClass = function (before, after) {
  this.classList.remove(before);
  this.classList.add(after);
};

// Open "details" element if called by id
function openTarget() {
  var hash = location.hash.substring(1);
  if (hash) var details = document.getElementById(hash);
  if (details && details.tagName.toLowerCase() === "details")
    details.open = true;
}
window.addEventListener("hashchange", openTarget);
openTarget();
