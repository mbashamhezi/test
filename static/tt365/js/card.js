function scrollLeft(card) {
    const imageContainer = card.querySelector('.image-container');
    const lastImage = imageContainer.lastElementChild;
    imageContainer.removeChild(lastImage);
    imageContainer.insertAdjacentElement('afterbegin', lastImage);
}

function scrollRight(card) {
    const imageContainer = card.querySelector('.image-container');
    const firstImage = imageContainer.firstElementChild;
    imageContainer.removeChild(firstImage);
    imageContainer.insertAdjacentElement('beforeend', firstImage);
}
