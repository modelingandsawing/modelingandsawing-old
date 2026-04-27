/**
 * Lightbox — full-screen image viewer.
 *
 * Usage:  lightbox.open(images, index)
 *
 * `images` is an array with at least a `full` URL property per entry.
 * Optional `alt` property is forwarded to the img element.
 *
 * Requires: script.js (defines switchClass on HTMLElement), lightbox.css.
 * Load this script after script.js, before any inline gallery scripts.
 *
 * To add lightbox to a gallery page:
 *   1. <link rel="stylesheet" href="./styles/lightbox.css" />
 *   2. <script src="./scripts/slideshow.js"></script> (after script.js)
 *   3. In the fetch callback, after building each image element, call:
 *      containerEl.style.cursor = "pointer";
 *      containerEl.addEventListener("click", function() {
 *        lightbox.open(groupImages, imageIndex);
 *      });
 */

class Lightbox {
  constructor() {
    this._images = [];
    this._index = 0;
    this._touchStartX = 0;
    this._keyHandler = this._onKey.bind(this);
    this._overlay = null;
    this._img = null;
    this._counter = null;
    this._build();
  }

  _build() {
    var el = document.createElement("div");
    el.id = "lightbox";
    el.className = "inactive";
    el.innerHTML =
      '<button class="lb-close" aria-label="Schließen">&#x2715;</button>' +
      '<button class="lb-prev"  aria-label="Zurück">&#x2039;</button>' +
      '<img class="lb-img" src="" alt="">' +
      '<button class="lb-next"  aria-label="Weiter">&#x203A;</button>' +
      '<span class="lb-counter"></span>';

    var self = this;
    el.querySelector(".lb-close").addEventListener("click", function() { self.close(); });
    el.querySelector(".lb-prev").addEventListener("click", function(e) {
      e.stopPropagation();
      self._go(-1);
    });
    el.querySelector(".lb-next").addEventListener("click", function(e) {
      e.stopPropagation();
      self._go(1);
    });
    el.addEventListener("click", function(e) {
      if (e.target === el) self.close();
    });
    el.addEventListener("touchstart", function(e) {
      self._touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });
    el.addEventListener("touchend", function(e) {
      var dx = e.changedTouches[0].screenX - self._touchStartX;
      if (Math.abs(dx) > 40) self._go(dx < 0 ? 1 : -1);
    }, { passive: true });

    document.body.appendChild(el);
    this._overlay = el;
    this._img = el.querySelector(".lb-img");
    this._counter = el.querySelector(".lb-counter");
  }

  open(images, index) {
    this._images = images;
    this._index = index;
    this._update();
    this._overlay.switchClass("inactive", "active");
    document.addEventListener("keydown", this._keyHandler);
    document.body.style.overflow = "hidden";
  }

  close() {
    this._overlay.switchClass("active", "inactive");
    document.removeEventListener("keydown", this._keyHandler);
    document.body.style.overflow = "";
  }

  _go(delta) {
    this._index = (this._index + delta + this._images.length) % this._images.length;
    this._update();
  }

  _update() {
    var img = this._images[this._index];
    this._img.src = img.full;
    this._img.alt = img.alt || "";
    var multi = this._images.length > 1;
    this._counter.textContent = multi ? (this._index + 1) + " / " + this._images.length : "";
    this._overlay.querySelector(".lb-prev").hidden = !multi;
    this._overlay.querySelector(".lb-next").hidden = !multi;
  }

  _onKey(e) {
    if (e.key === "ArrowLeft")  this._go(-1);
    if (e.key === "ArrowRight") this._go(1);
    if (e.key === "Escape")     this.close();
  }
}

const lightbox = new Lightbox();
