import { getRandomNumber, getElement } from './utils.js';
import { getRandomUpperChar, getRandomLowerChar, getRandomSpecialCharacter} from './randomChars.js';

export function generatePassword(length) {
    const optionsCheck = {
        upperLetters: getElement('#upper-input').checked,
        lowerLetters: getElement('#lower-input').checked,
        numbers: getElement('#numbers-input').checked,
        specialCharacters: getElement('#symbols-input').checked
    }

    const optionsFunctionMap = {
        upperLetters: getRandomUpperChar,
        lowerLetters: getRandomLowerChar,
        numbers: () => getRandomNumber(0, 9),
        specialCharacters: getRandomSpecialCharacter
    }

    let passwordArray = Array();

    for (let c = 0; c < length; c++) {
        let subPassword = '';
        let optionsChecked = 0;

        for (let option in optionsFunctionMap) {
            if (optionsCheck[option]) {
                optionsChecked += 1;

                subPassword += optionsFunctionMap[option]();
            }
        }

        let randomNumber = getRandomNumber(0, optionsChecked);
        passwordArray.push(subPassword[randomNumber]);
    }

    return passwordArray.join('');
}
