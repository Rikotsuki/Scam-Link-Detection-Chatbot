import pkg from "jsonwebtoken";
import { config } from "../config.js";
const { verify } = pkg;

export const verifyToken = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: "Access token required" });
  }
  
  try {
    const decoded = verify(token, config.JWT_SECRET);
    req.user = decoded;
    next();
  } catch (error) {
    console.error('Token verification failed:', error.message);
    return res.status(401).json({ error: "Invalid or expired token" });
  }
};

export const optionalAuth = (req, res, next) => {
  const token = req.headers.authorization?.split(' ')[1];
  
  if (token) {
    try {
      const decoded = verify(token, config.JWT_SECRET);
      req.user = decoded;
    } catch (error) {
      // Token is invalid, but we'll continue without user info
      console.warn('Invalid token in optional auth:', error.message);
    }
  }
  
  next();
}; 