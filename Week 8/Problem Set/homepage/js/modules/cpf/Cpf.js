export default class Cpf {
    constructor(cpf) {
        this.cpf = cpf;
    }

    verify() {
        let formattedCpf = this.cpf.replace(/\D+/g, '');
        if (formattedCpf.length != 11 || typeof formattedCpf === 'undefined') {
            return false;
        }

        let cpfArray = Array.from(formattedCpf.slice(0, -2));
        this.discoverDigit(cpfArray, 10);
        this.discoverDigit(cpfArray, 11);

        if (String(cpfArray.join('')) !== String(formattedCpf)) return false;
        return true;
    }

    discoverDigit(array, value) {
        let sum = 0;

        array.reduce((accumulator, element) => {
            sum += Number(element) * accumulator;
            return accumulator -= 1;
        }, value);

        let digit = 11 - (sum % 11);
        array.push(digit > 9 ? 0 : digit);
    }

    generate() {
        let cpfArray = Array()
        while (cpfArray.length < 9) {
            let randomNumber = Math.floor(Math.random() * 10);
            cpfArray.push(randomNumber);
        }

        this.discoverDigit(cpfArray, 10);
        this.discoverDigit(cpfArray, 11);

        let formattedCpf = String(cpfArray.join(''));

        formattedCpf = formattedCpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/g, "$1.$2.$3-$4");
        return formattedCpf;
    }
}
