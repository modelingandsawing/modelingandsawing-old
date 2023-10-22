class Slideshow {
  slideIndex = 1;

  activate = (i = 1) => {
    document.querySelector("div#slideshow").switchClass("inactive", "active");
    if (i > 1) {
      this.slideIndex = i;
      this.showSlide();
    }
  };

  deactivate = () => {
    document.querySelector("div#slideshow").switchClass("active", "inactive");
  };

  switchSlide = (n) => {
    this.showSlide((this.slideIndex += n));
  };

  showSlide = (n = 1) => {
    const x = document.getElementsByClassName("slideshow-elem");
    if (n > x.length) {
      this.slideIndex -= x.length;
    }
    if (n < 1) {
      this.slideIndex = x.length;
    }
    for (let i = 0; i < x.length; i++) {
      x[i].switchClass("active", "inactive");
    }
    x[this.slideIndex - 1].switchClass("inactive", "active");
  };
}

const slideshow = new Slideshow();

document.querySelector("div.controls").addEventListener("click", (e) => {
  if (!e.target.classList.contains("controls")) return;
  slideshow.deactivate();
});
