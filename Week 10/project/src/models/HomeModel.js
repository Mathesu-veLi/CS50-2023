const mongoose = require('mongoose');

const HomeSchema = new mongoose.Schema({
    title: { type: String, required: true },
    desc: String
});

const HomeModel = mongoose.model('Home', HomeSchema);

class Home {

};

module.exports = Home;
