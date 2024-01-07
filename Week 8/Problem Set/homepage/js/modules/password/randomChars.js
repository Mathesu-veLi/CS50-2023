import { getRandomNumber } from './utils.js';

export function getRandomUpperChar() {
    const randomNumber = getRandomNumber(65, 90);
    const randomUpperChar = String.fromCharCode(randomNumber);

    return randomUpperChar;
}

export function getRandomLowerChar() {
    const randomNumber = getRandomNumber(97, 122);
    const randomLowerChar = String.fromCharCode(randomNumber);

    return randomLowerChar;
}

export function getRandomSpecialCharacter() {
    let subPassword = Array();

    let specialCharactersRangesSet = [[33, 47], [58, 64], [94, 96], [123, 126]];
    for (let c = 0; c < specialCharactersRangesSet.length; c++) {
        let randomNumber = getRandomNumber(specialCharactersRangesSet[c][0], specialCharactersRangesSet[c][1]);
        let randomSpecialCharacter = String.fromCharCode(randomNumber);

        subPassword.push(randomSpecialCharacter);
    }

    const randomSpecialCharacter = subPassword[getRandomNumber(0, 4)];
    return randomSpecialCharacter;
}
