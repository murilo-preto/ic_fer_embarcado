import ws from "ws";

const client = new ws("ws://localhost:3000");

client.onopen = (event) => {
  client.send("Hello");
};

client.onmessage = (event) => {
  console.log(event.data);
};
