import { generateIp } from './modules/ip/main.js';

const ip = document.querySelector("#generator");
const form = document.querySelector("form");

form.addEventListener('submit', (e) => {
    e.preventDefault();

    ip.innerHTML = generateIp();
});
