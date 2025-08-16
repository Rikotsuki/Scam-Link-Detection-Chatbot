import pkg from "jsonwebtoken";
const {sign} = pkg;

export const genToken = ({_id}) => {
    return sign(
      { id: _id},
      process.env.JWT_SECRET,
      { expiresIn: process.env.JWT_EXPIRES_IN || "1d" }
    );
}