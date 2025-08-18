import express, { json } from 'express';
import { configDotenv } from 'dotenv';
import { connect } from 'mongoose';
import authRoutes from './routes/auth.js';
import privateRoutes from './routes/private.js';
import phishguardRoutes from './routes/phishguard.js';
import { config } from './config.js';

configDotenv();

const app = express();
const PORT = config.PORT;

app.use(json());
app.use('/auth', authRoutes);
app.use('/private', privateRoutes);
app.use('/api/phishguard', phishguardRoutes);

connect(config.DB_URL)
.then(console.log('DB connected'))
.catch(e=>console.log(e));

app.listen(PORT,()=>{
    console.log(`server running at localhost:${PORT}` );
});