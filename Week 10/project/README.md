# Phonebook

## Description:
My final project for the CS50 is Phonebook, which allows you to save your contacts so you don't forget information about them.

To start saving contacts, you need to register or log in to the site.

To register, you need your password to be at least 3 characters long (Don't worry! Your password is encrypted before it goes into the database, so it's safe!) and provide a valid email address.

By clicking on 'Add Contact' on the index page, you can fill in the fields:
Name
Last name
Email address
Phone
(You cannot add 2 contacts with the same phone number, but you can register 2 contacts with the same email address)
(You need add a email OR a phone number, not necessarily both)

After registering a contact, you can see the registered data on the index page, along with 2 action links, edit and delete, which, as the name suggests, edit the contact's data and delete the contact, respectively.

When you log in to Phonebook with the same account on another device, you can see that the contacts registered on the previous device are also shown on the other one, as the contacts are saved in a remote database
#### Video Demo:

https://youtu.be/01q8oSUQCEQ
## Explain the project

Parts of the code that I think are important to explain

### Database
Contacts and users are saved using MongoDB via `mongoose`.

### Registering contacts in the database

#### Validation

Only the data provided for the contact record needed to be validated:

<ul>
<li>If the name field was empty</li>

```javascript
if(!this.body.name) {
    this.errors.push('Name field cannot be empty');
}
```

<li>If the email and phone are empty</li>

```javascript
if(!this.body.email && !this.body.tel) {
    this.errors.push('Email or telephone field cannot be empty');
};
```

<li>If the email is empty or not valid</li>

```javascript
if (this.body.email && !validator.isEmail(this.body.email)) {
    this.errors.push('Invalid E-mail');
}
```

</ul>

The email was validated using the `isEmail` function from the `validator` package.

#### `createdBy`
When you register a contact, it will go to the database with its data and a `createdBy` column, which will have the value of the email of the user currently logged in, so that he can see on the index page only the contacts registered by his account


### Editing contacts
The data is edited on the same page as the contact's registration, changing only the route to the page where the contact's `id` is added. The contact's data is loaded based on this `id` of the route

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`CONNECTIONSTRING`
## Tech Stack

**Client:** Bootstrap 5

**Server:** Node, Express

