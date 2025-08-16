import mongoose, { Schema } from "mongoose";

const userSchema = new Schema ({
    firstName: {type: String},
    lastName: {type: String},
    userName: {type: String, required: true, unique: true},
    email: {type: String, required: true, unique: true},
    password: {type: String, required: true},
    createdAt: {type: Date, default: Date.now()}

});

export default mongoose.model('user', userSchema);