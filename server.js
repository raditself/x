
const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
const port = 3001;

app.use(bodyParser.json());

app.post('/chat', async (req, res) => {
  const { message } = req.body;

  // TODO: Replace with actual interaction with the Crataco/stablelm-2-1_6b-chat-imatrix-GGUF model
  const botResponse = `Response from Crataco/stablelm-2-1_6b-chat-imatrix-GGUF model to: ${message}`;

  res.json({ response: botResponse });
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
