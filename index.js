require("dotenv").config(); // NOTE: for recognize files -> .env || .env.*
const express = require("express");
const {spawn} = require("child_process");

const cors = require("cors");
const app = express();

app.use(cors());

const port = process.env.PORT_LOCAL || 3000;

app.get("/wsc-ketal", (req, res) => {
  const param = req.query.param;
  console.log("PARAM", param);
  const process = spawn("python3", ["wsc.ketal.py", param]);
  process.stdout.on("data", (data) => {
    console.log(`stdout: ${data}`);
    res.json(JSON.parse(data));
  });
  process.stderr.on("data", (data) => {
    console.log(`stderr: ${data}`);
    res.send(data);
  });
  process.on("close", (code) => {
    console.log(`child process exited with code ${code}`);
  });
});

app.get("/my-endpoint", (req, res) => {
  const param = req.query.someparam;
  console.log("PARAM", param);

  const process = spawn("python3", ["script.py", param]);
  process.stdout.on("data", (data) => {
    console.log(`stdout: ${data}`);
    res.json({message: data.toString()});
  });
  process.stderr.on("data", (data) => {
    console.log(`stderr: ${data}`);
    res.send(data);
  });
  process.on("close", (code) => {
    console.log(`child process exited with code ${code}`);
  });
});

app.listen(port, () => {
  console.log(`Listening on port http://localhost:${port}`);
});
