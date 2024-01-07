const mongoose = require('mongoose');
const validator = require('validator');

const ContactSchema = new mongoose.Schema({
    name: { type: String, required: true },
    surname: { type: String, required: false, default: '' },
    email: { type: String, required: false, default: ''  },
    tel: { type: String, required: false, default: ''  },
    createdBy: {type: String, required: true},
    createdIn: { type: Date, default: Date.now },
});

const ContactModel = mongoose.model('Contact', ContactSchema);

function Contact(body, userEmail) {
    this.body = body;   
    this.errors = [];
    this.contact = null;
    this.userEmail = userEmail;
};

Contact.prototype.register = async function () {
    await this.validate();

    const contactExists = await ContactModel.findOne({ tel: this.body.tel,  createdBy: this.userEmail});
    if (contactExists) {
        this.errors.push('Phonenumber already registred. You might want to go to the home page and edit the existing contact')
    }

    if(this.errors.length > 0) return;
    this.contact = await ContactModel.create(this.body);
};

Contact.prototype.validate = async function () {
    this.cleanUp();

    if(!this.body.name) {
        this.errors.push('Name field cannot be empty');
    }

    if(!this.body.email && !this.body.tel) {
        this.errors.push('Email or telephone field cannot be empty');
    };

    if (this.body.email && !validator.isEmail(this.body.email)) {
        this.errors.push('Invalid E-mail');
    }
};

Contact.prototype.cleanUp = function () {
    for (const key in this.body) {
        if (typeof this.body[key] !== 'string') {
            this.body[key] = '';
        };
    };

    this.body = {
        name: this.body.name,
        surname: this.body.surname,
        email: this.body.email,
        tel: this.body.tel,
        createdBy: this.body.createdBy
    };
};

Contact.prototype.edit = async function(id) {
    if(typeof id !== 'string') return;
    this.validate();
    if(this.errors.length > 0) return;
    this.contact = await ContactModel.findByIdAndUpdate(id, this.body, { new: true });
};

Contact.searchById = async function(id) {
    if(typeof id !== 'string') return;
    return await ContactModel.findById(id);
};

Contact.searchContacts = async function(userEmail) {
    const contacts = await ContactModel.find({createdBy: userEmail}).sort({ createdIn: 1 });
    return contacts;
};

Contact.delete = async function(id) {
    if(typeof id !== 'string') return;
    const contact = await ContactModel.findOneAndDelete({_id: id});
    return contact;
}

module.exports = Contact;
