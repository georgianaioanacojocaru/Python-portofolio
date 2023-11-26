let currentIndex = 0;
const totalImages = document.querySelectorAll('.carousel-image').length;
const imageContainer = document.getElementById('image-container');

function updateCarousel() {
  imageContainer.style.transform = `translateX(${-currentIndex * 100}%)`;
}

function nextImage() {
  currentIndex = (currentIndex + 1) % totalImages;
  updateCarousel();
}

function prevImage() {
  currentIndex = (currentIndex - 1 + totalImages) % totalImages;
  updateCarousel();
}

// Optional: Auto slide to the next image every 3 seconds
setInterval(nextImage, 5000);