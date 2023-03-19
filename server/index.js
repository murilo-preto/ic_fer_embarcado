import express from "express";
import { WebSocket, WebSocketServer } from "ws";
import { v4 } from "uuid";

const app = express();
const port = process.env.PORT || 3000;

app.set("view engine", "ejs");
app.use(express.json());

const wsServer = new WebSocketServer({ noServer: true });

wsServer.on("connection", function (connection) {
  const userId = v4();
  console.log("Recieved a new connection");
  clients[userId] = connection;
  console.log(`${userId} connected.`);

  connection.on("close", () => handleDisconnect(userId));

  connection.on("message", function (message) {
    message = message.toString();
    console.log(message);
    connection.send("Server: Connection established");
  });
});

const server = app.listen(port);

server.on("upgrade", (req, socket, head) => {
  wsServer.handleUpgrade(req, socket, head, (ws) => {
    wsServer.emit("connection", ws, req);
  });
});

const clients = {};
let editorContent = null;

const typesDef = {
  USER_EVENT: "userevent",
  CONTENT_CHANGE: "contentchange",
};

function broadcastMessage(json) {
  // We are sending the current data to all connected clients
  const data = JSON.stringify(json);
  for (let userId in clients) {
    let client = clients[userId];
    if (client.readyState === WebSocket.OPEN) {
      client.send(data);
    }
  }
}

function handleDisconnect(userId) {
  console.log(`${userId} disconnected.`);
  delete clients[userId];
}

app.get("/", function (req, res) {
  res.render("pages/index");
});

app.get("/facialexpressions", function (req, res) {
  res.render("pages/facialexpressions");
});

app.get("/about", function (req, res) {
  res.render("pages/about");
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

const fexList = [{ id: 1, fex: "happy", date: "2023-1-9", time: "17:58:34" }];

let data = generateData();

function generateData() {
  let randomData = [
    Math.floor(Math.random() * 10) + 1,
    Math.floor(Math.random() * 10) + 1,
    Math.floor(Math.random() * 10) + 1,
    Math.floor(Math.random() * 10) + 1,
    Math.floor(Math.random() * 10) + 1,
    Math.floor(Math.random() * 10) + 1,
    Math.floor(Math.random() * 10) + 1,
  ];

  return randomData;
}

setInterval(function lambda() {
  data = generateData();
  broadcastMessage(data);
}, 1000);
