import express, { json } from 'express';
import cors from 'cors';
import { configDotenv } from 'dotenv';
import { connect } from 'mongoose';
import authRoutes from './routes/auth.js';
import privateRoutes from './routes/private.js';
import phishguardRoutes from './routes/phishguard.js';
import animeRoutes from './routes/anime.js';
import { config } from './config.js';

configDotenv();

const app = express();
const PORT = config.PORT;

// Enable CORS for frontend integration
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3001',
  credentials: true
}));

app.use(json());
app.use('/auth', authRoutes);
app.use('/private', privateRoutes);
app.use('/api/phishguard', phishguardRoutes);
app.use('/api/anime', animeRoutes);

connect(config.DB_URL)
.then(console.log('DB connected'))
.catch(e=>console.log(e));

app.listen(PORT,()=>{
    console.log(`server running at localhost:${PORT}` );
});