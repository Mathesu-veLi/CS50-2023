export function getRandomNumber(min, max) {
    return Math.floor(Math.random() * ((min - 1) - max + 1)) + max;
}

export function getElement(selector) {
    return document.querySelector(selector);
}
