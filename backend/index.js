const express = require('express');
const app = express();
const PORT = 5000;

app.get('/', (req, res) => {
  res.send('Marketly backend ishlayapti!');
});

app.listen(PORT, () => {
  console.log(`Server ${PORT} portda ishlayapti`);
});
