require("dotenv").config() // NOTE: for recognize files -> .env || .env.*
const express = require('express')
const cors = require("cors")
const app = express()

app.use(cors())

const port = process.env.PORT || 3000

app.get('/', (req, res) => {
  res.send('Hello World with Express!')
})

app.listen(port, () => {
  console.log(`Listening on port http://localhost:${port}`)
})