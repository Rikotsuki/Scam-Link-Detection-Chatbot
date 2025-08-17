import { body, validationResult } from "express-validator";
import user from "../models/user.js";
export const authValidate = [
    body("email")
      .trim()
      .isEmail()
      .withMessage("A valid email is required"),
  
    body("password")
      .isLength({ min: 5 })
      .withMessage("Password must be at least 5 characters long"),

    body("email")
        .custom(async (value)=>{
            const exist = await user.findOne({email : value});
            if(exist){
                throw new Error("Email already in used.");
            }
        }),

    body("userName")
        .custom(async (value)=>{
            const exist = await user.findOne({userName : value}); 
            if(exist){
                throw new Error("Username already in used.");
            }
        }),

    // final gate
    (req, res, next) => {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return res.status(400).json({ error: errors.array() });
      }
      next();
    },
  ];