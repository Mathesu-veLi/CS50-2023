import { generatePassword } from './modules/password/main.js';



const form = document.querySelector('form');
form.addEventListener('submit', (e) => {
    e.preventDefault();
})

const password = document.querySelector('.response');
const input = document.querySelector('#quantity-input');
password.value = generatePassword(input.value);

input.addEventListener('change', (e) => {
    if (input.value < 4) {
        input.value = 4;
    }

    range.value = input.value;
    password.value = generatePassword(input.value);
});

const range = document.querySelector('#quantity-range');
range.addEventListener('change', (e) => {
    input.value = range.value;
    password.value = generatePassword(range.value);
});

const checks = document.querySelectorAll('#checks > div > input');
let optionsChecked = 0;
checks.forEach((element) => {
    if (element.checked) optionsChecked += 1;

    element.addEventListener('change', (e) => {
        if (!element.checked) optionsChecked -= 1;
        else optionsChecked += 1;

        if (optionsChecked === 0) {
            element.checked = true;
            optionsChecked = 1;
        };
    })
});
