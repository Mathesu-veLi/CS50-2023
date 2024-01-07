const Contact = require('../models/ContactModel');

exports.index = async (req, res) => {
    try {
        contacts = await Contact.searchContacts(req.session.user.email);
    } catch (e) {
        contacts = await Contact.searchContacts('');
    }

    res.render('index', { contacts });
};
