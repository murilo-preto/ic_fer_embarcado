import express from "express";
import { WebSocket, WebSocketServer } from "ws";
import { v4 } from "uuid";
import mysql from "mysql";

const app = express();
const port = process.env.PORT || 3000;

app.set("view engine", "ejs");
app.use(express.json());

// ---------- SQL ----------
// Connect to SQL
var connection = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "password",
  database: "centerfex_2023",
});

// Log any connection error
connection.connect(function (err) {
  if (err) throw err;
  console.log("Connected as id " + connection.threadId + " to query data");
});

// Get data from SQL
function selectDataSQL (){
  let selectQuery = "SELECT facial_expressions,facial_expression_id, COUNT(*) AS contagem FROM detection JOIN fex_table ON (detection.facial_expression_id=fex_table.id) GROUP BY facial_expression_id"
connection.query(selectQuery, function (err, result, __) {
  if (err) throw err;

  let fexCount = {
    "disgust": 0,
    "happy": 0,
    "fear": 0,
    "neutral": 0,
    "angry": 0,
    "surprise": 0,
    "sad": 0,
  };

  let toGraphFex = [];

  for (let i of result){
    let row = Object.assign({}, i);
    fexCount[row.facial_expressions] = row.contagem;
  }

  for (let key in fexCount){
    toGraphFex.push(fexCount[key]);
  }

  console.log(toGraphFex);
  broadcastMessage(toGraphFex);
  });
}

// Send data to SQL
let queryBuffer = [];
function insertDataSQL (queryBuffer){
  // relational query
  let valuesQuery = concatValuesQuery(queryBuffer);
  let detectionQuery = `INSERT INTO detection (id, facial_expression_id, date_and_time, network_id, location_id) VALUES ${valuesQuery}`;

  // send detected data to database
  connection.query(detectionQuery, function (err, result, __) {
    if (err) throw err;
  });
};

// Format data to SQL VALUES format
function concatValuesQuery (queryBuffer){ // queryBuffer to SQL VALUES
  let queryCache = new String();
  for (let i in queryBuffer){
    let fexQuery = `(SELECT id FROM fex_table WHERE facial_expressions="${queryBuffer[i].detectedFex}")`;
    let networkQuery = `(SELECT id FROM network_address WHERE mac_address="${queryBuffer[i].detectedMacAddress}")`;
    let locationQuery = `(SELECT id FROM locations WHERE city="${queryBuffer[i].detectedCity}")`;

    if (i==0){
      queryCache += `(null, ${fexQuery}, (SELECT UTC_TIMESTAMP), ${networkQuery}, ${locationQuery})`;
    }
    else{
      queryCache += `,(null, ${fexQuery}, (SELECT UTC_TIMESTAMP), ${networkQuery}, ${locationQuery})`;
    }
  }
  return queryCache;
}
// -------------------------


// ---------- Eventos Webcksocket ----------
const wsServer = new WebSocketServer({ noServer: true });
wsServer.on("connection", function (connection) {
  const userId = v4();
  console.log("Received a new connection");
  clients[userId] = connection;
  console.log(`${userId} connected.`);

  connection.on("close", () => handleDisconnect(userId));

  connection.on("message", function (message) {
    message = message.toString();
    console.log(message);
    connection.send("Server: Connection established");
  });
});
// -----------------------------------------


// ---------- Eventos HTTP ----------
const server = app.listen(port);
server.on("upgrade", (req, socket, head) => {
  wsServer.handleUpgrade(req, socket, head, (ws) => {
    wsServer.emit("connection", ws, req);
  });
});

const clients = {};

function broadcastMessage(json) {
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
  res.send(queryBuffer);
});

app.post("/api/facialexpressions", (req, res) => {
  // Atualiza fexList com dados recebidos em JSON
  if (!req.body.fex) {
    // Validação de input
    // 400 Bad Request
    res.status(400).send("Facial expression is required");
    return;
  }

  const fex = {
    detectedFex: req.body.fex,
    detectedMacAddress: req.body.macaddress,
    detectedCity: "SantoAndre",
  };

  res.status(200).send(fex);
  queryBuffer.push(fex); // Atualiza base de dados
  console.log(fex);
});

setInterval(function () {
  if (Object.keys(queryBuffer).length>4){
    insertDataSQL(queryBuffer);
    queryBuffer = [];
  }
}, 3000);

setInterval(selectDataSQL, 3000);
