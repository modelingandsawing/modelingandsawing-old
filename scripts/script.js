// Redirect to another page
function redirect(url) {
  console.log("🚀 ~ file: script.js:3 ~ redirect ~ url:", url);
  window.location.href = url;
}

// Show the language selection menu
function showLanguageMenu() {
  document.querySelector("div#change-language").style.visibility = "visible";
}

function showNavigationMenu() {
  document.querySelector("div#navigation-menu").style.visibility = "visible";
}

document.onclick = (e) => {
  // Hide the language selection menu
  if (e.target.id !== "icon-change-language") {
    document.querySelector("div#change-language").style.visibility = "hidden";
  }

  // Hide the navigation menu
  if (e.target.id !== "icon-navigation-menu") {
    document.querySelector("div#navigation-menu").style.visibility = "hidden";
  }
};

HTMLElement.prototype.switchClass = function (before, after) {
  this.classList.remove(before);
  this.classList.add(after);
};
