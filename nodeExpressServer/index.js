const express = require("express");
const app = express();

app.use(express.json()); // JSON Middleware

const fexList = [{ id: 1, fex: "happy", date: "2023-1-9", time: "17:58:34" }];

app.get("/", (req, res) => {
  res.send("/api/facialexpressions for further request");
});

app.get("/api/facialexpressions", (req, res) => {
  res.send(fexList);
});

app.get("/api/facialexpressions/:id", (req, res) => {
  const fex = fexList.find((c) => c.id === parseInt(req.params.id));
  if (!fex) res.status(404).send("Facial expression with given ID not found");
  res.send(fex);
});

app.post("/api/facialexpressions", (req, res) => {
  // Atualiza fexList com dados recebidos em JSON
  if (!req.body.fex) {
    // Validação de input
    // 400 Bad Request
    res.status(400).send("Facial expression is required");
    return;
  }

  var today = new Date();
  var date =
    today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate();
  var time =
    today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();

  const fex = {
    id: fexList.length + 1,
    fex: req.body.fex,
    date: date,
    time: time,
  };

  res.status(200).send(fex);
  fexList.push(fex); // Atualiza base de dados
  console.log(fex);
});

// PORT = environment variables -> changes dinamically -> Necessário para sites de hospedagem
const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Listening on port ${port}`));
