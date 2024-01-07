const Contact = require('../models/ContactModel');

exports.index = (req, res) => {
    res.render('contact', {
        contact: {}
    });
};

exports.register = async (req, res) => {
    try {
        const contact = new Contact(req.body, req.session.user["email"]);
        await contact.register();

        if (contact.errors.length > 0) {
            req.flash('errors', contact.errors);
            req.session.save(() => res.redirect('/contact'));
            return;
        };

        if (contact.exists) {
            req.flash('errors', 'Phonenumber already registred. You might want to go to the home page and edit the existing contact')
            req.session.save(() => res.redirect(`/contact`))
            return;
        }

        req.flash('success', 'Contact registered successfully');
        req.session.save(() => res.redirect('/'));
        return;
    } catch (e) {
        console.log(e);
        return res.render('404');
    };
};


exports.editIndex = async function (req, res) {
    if (!req.params.id) return res.render('404');

    const contact = await Contact.searchById(req.params.id);
    if (!contact) return res.render('404');

    res.render('contact', { contact });
};

exports.edit = async function (req, res) {
    try {
        if (!req.params.id) return res.render('404');
        const contact = new Contact(req.body);
        await contact.edit(req.params.id);

        if (contact.errors.length > 0) {
            req.flash('errors', contact.errors);
            req.session.save(() => res.redirect('/contact'));
            return;
        };

        req.flash('success', 'Contact edited successfully');
        req.session.save(() => res.redirect('/'));
        return;
    } catch (e) {
        console.log(e);
        res.render('404');
    };
};

exports.delete = async function(req, res) {
    if (!req.params.id) return res.render('404');

    const contact = await Contact.delete(req.params.id);
    if (!contact) return res.render('404');

    req.flash('success', 'Contact deleted successfully');
    req.session.save(() => res.redirect('/'));
    return;
}
