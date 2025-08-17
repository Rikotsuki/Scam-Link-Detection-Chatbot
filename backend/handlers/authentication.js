import { genToken } from "../utils/token.js";
import { hash } from "bcryptjs";
import user from "../models/user.js";
import { compare } from "bcryptjs";

export const register = async(req, res) => {
  try {

    const hashed = await hash(req.body.password, 10);

    const newUser = new user({
        firstName : req.body.firstName,
        lastName : req.body.lastName,
        userName : req.body.userName,
        email : req.body.email,
        password: hashed,
    });
    await newUser.save();

    return res.status(201).json({ message: "User registered successfully.",token: genToken(newUser)});
  } catch (err) {
    console.error("Register error:", err);
    return res.status(500).json({ error: "Server error." });
  }
}



export const login = async (req, res)=> {
    try {
        const { email, password } = req.body;
    
        // Check if user exists
        const loginUser = await user.findOne({ email });
        if (!loginUser) {
          return res.status(401).json({ error: "Invalid email or password." });
        }
    
        // Check password
        const isMatch = await compare(password, loginUser.password);
        if (!isMatch) {
          return res.status(401).json({ error: "Invalid email or password." });
        }
    
        // Generate JWT token
        const token = genToken(loginUser);
    
        // Respond with success and user info (omit password!)
        res.status(200).json({
          message: "Login successful",
          token,
        });
    } catch (err) {
        console.error("Login error:", err);
        return res.status(500).json({error: "Server error."});
    }
}