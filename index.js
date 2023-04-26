require("dotenv").config(); // NOTE: for recognize files -> .env || .env.*
const express = require("express");
const {spawn} = require("child_process");

const cors = require("cors");
const app = express();

app.use(cors());

const port = process.env.PORT_LOCAL || 3000;

app.get("/wsc-ketal", (req, res) => {
  // const param = req.query.param;
  const paramUrl = req.query.requestUrl;
  console.log("paramUrl.toString()>>>>>", paramUrl.toString());

  const baseUrl = "https://www.ketal.com.bo";

  // WIP: Validation
  if (!paramUrl.toString().includes(baseUrl)) {
    return res.status(422).json({
      message: "Verifique que los datos sean válidos",
      validation: [
        {
          field: `URL`, // requestUrl
          message: `La url que envíe debe contener ${baseUrl}.`,
        },
      ],
    });
  }

  // Array ["", "/"] => length = 1 || ["", "some-category"]  => length > 1
  // Apply length to String
  if (paramUrl.split(baseUrl)[1].length <= 1) {
    return res.status(422).json({
      message: "Verifique que los datos sean válidos",
      validation: [
        {
          field: `URL`, // requestUrl
          /* eslint-disable-next-line max-len */
          message: `La url que envíe debe ser de la página de búsqueda/filtrado (por ejemplo: ${baseUrl}alguna-categoria). NO puede ser de la página principal, sin embargo, si desea agregar el soporte/funcionalidad de esta página, ¡contáctenos! `,
        },
      ],
    });
  }

  /* const pythonProcess = spawn("python3", [
    "/path/to/script.py",
    "param1",
    "param2",
  ]); */

  // WIP: pythonProcess
  const process = spawn("python3", ["wsc.ketal.py", paramUrl]);
  process.stdout.on("data", (data) => {
    // console.log(`stdout: ${data}`);
    return res.json(JSON.parse(data));
  });
  process.stderr.on("data", (data) => {
    console.log(`stderr: ${data}`);
    return res.status(422).json({
      message: "Verifique que los datos sean válidos",
      validation: [
        {
          field: `URL`, // requestUrl
          message: `${data}`,
        },
      ],
    });
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

// app.listen(port, "127.0.0.1", (err) => {
app.listen(port, (err) => {
  if (err) {
    console.error(err);
    process.exit(1);
  }
  console.log(`Listening on port ${port}`);
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send("Algo salió mal!" + err);
});
