import { Router } from "express";
import { login, register } from "../handlers/authentication.js";
import { authValidate } from "../middlewares/validation.js";

const authRoutes = Router();

authRoutes.post('/register', authValidate, register);
authRoutes.post('/login', login);

export default authRoutes;