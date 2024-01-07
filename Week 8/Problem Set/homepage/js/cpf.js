import Cpf from './modules/cpf/Cpf.js'

const generatorForm = document.querySelector('#generator form');
generatorForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const cpf = new Cpf().generate();

    const p = document.querySelector(".response#generator");
    p.innerHTML = cpf;
})

const verificatorForm = document.querySelector('#verificator form');
verificatorForm.addEventListener('submit', (e) => {
    e.preventDefault();

    let cpf = document.querySelector('#verificator #cpf').value;
    cpf = new Cpf(cpf);

    const p = document.querySelector(".response#verificator")
    if (!cpf.verify())
    {
        p.innerHTML = cpf.cpf == '' ? "Insert a CPF!" : "Invalid!"
        p.style.color = "#f23";
    } else {
        p.innerHTML = "Valid!"
        p.style.color = "#32f";
    }

    p.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
})
