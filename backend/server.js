
const express = require('express');
const OpenAI = require("openai");
const { OpenAIApi } = require('openai');
require('dotenv').config();

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

// Assuming OpenAIApi() constructor takes an object with apiKey
const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY,
  });
  
app.post('/ask', async (req, res) => {
  const prompt = req.body.question;
  try {
    const chatCompletion = await openai.chat.completions.create({
        messages: [{ role: "user", content: "Say this is a test" }],
        model: "gpt-3.5-turbo",
    });
    res.json({ answer: response.data.choices[0].message.content });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Error getting response from OpenAI" });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
