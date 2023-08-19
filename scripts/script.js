// Redirect to another page
function redirect(url) {
    window.location.href = url;
};

// Show the language selection menu
function showLanguageMenu() {
    document.querySelector('div#select-language').style.display = 'block';
};

// Hide the language selection menu
document.onclick = (e) => {
    if (e.target.id == 'title-change-language') return;
    document.querySelector('div#select-language').style.display = 'none';
};

HTMLElement.prototype.switchClass = function (before, after) {
    this.classList.remove(before);
    this.classList.add(after);
};