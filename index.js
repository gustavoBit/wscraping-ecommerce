require("dotenv").config() // NOTE: for recognize files -> .env || .env.*
const express = require('express')
// const { spawnSync } = require('child_process'); // TODO: PENDING test
// const { spawn } = require('node:child_process'); // TODO: PENDING test
const { execFile } = require("child_process");

const cors = require("cors")
const app = express()

app.use(cors())

const port = process.env.PORT || 3000

app.get('/wsc-ketal', (req, res) => {
  const pythonFilePath = "./dist/scraping.ketal/scraping.ketal"; // EXEC GENERATED with PyINSTALLER from other _project Python
  execFile(pythonFilePath, (err, stdout, stderr) => {
    if (err) {
      console.error(err);
      return;
    }
    // console.log('stdout >>>', stdout);
    res.json(JSON.parse(stdout))
  });
})

app.listen(port, () => {
  console.log(`Listening on port http://localhost:${port}`)
})