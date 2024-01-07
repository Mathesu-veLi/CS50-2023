export function generateIp() {
    let ip = Array();
    for (let c = 0; c < 4; c++)
    {
        let randomNumber = getRandomNumber(0, 255);
        ip.push(randomNumber);
    }
    return ip.join(".");
}

function getRandomNumber(min, max) {
    return Math.floor(Math.random() * ((min - 1) - max + 1)) + max;
}
