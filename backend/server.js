import express from 'express';
//import { agent } from './index.js'; // Import your agent function

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json()); // for parsing application/json

app.post('/chat', async (req, res) => {
  try {
    const userInput = req.body.userInput;
    //const response = await agent(userInput);
    const fixedResponse = "This is a test response message";
    res.json({ message: fixedResponse });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});