
var express = require('express')
var bodyParser = require('body-parser')


var app = express()
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({extended: true}))




app.get('/', (req, res) => {
    res.end("This is a test server for autogen.")
})

app.post('/basic_post', (req, res) => {
    res.json(req.body)
})

app.listen(process.env.port || 3000, () => {
    console.log("Now listening.")
})