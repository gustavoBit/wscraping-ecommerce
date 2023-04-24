require("dotenv").config(); // NOTE: for recognize files -> .env || .env.*
const express = require("express");
// const { spawnSync } = require('child_process'); // TODO: PENDING test
const {execFile, spawn} = require("child_process");

const cors = require("cors");
const app = express();

app.use(cors());

const port = process.env.PORT_LOCAL || 3000;

app.get("/scraping-ketal", (req, res) => {
  /* eslint-disable-next-line max-len */
  const pythonFilePath = "./dist/scraping.ketal/scraping.ketal"; // EXEC GENERATED with PyINSTALLER from other _project Python
  execFile(pythonFilePath, (err, stdout, stderr) => {
    if (err) {
      console.error(err);
      return;
    }
    // console.log('stdout >>>', stdout);
    res.json(JSON.parse(stdout));
  });
});

app.get("/wsc-ketal", (req, res) => {
  const param = req.query.param;
  console.log("PARAM", param);
  const process = spawn("python3", ["wsc.ketal.py", param]);
  process.stdout.on("data", (data) => {
    console.log(`stdout: ${data}`);
    res.send(data);
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
    res.send(data);
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
