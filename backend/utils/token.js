import pkg from "jsonwebtoken";
import { config } from "../config.js";
const {sign} = pkg;

export const genToken = ({_id}) => {
    return sign(
      { id: _id},
      config.JWT_SECRET,
      { expiresIn: config.JWT_EXPIRES_IN }
    );
}