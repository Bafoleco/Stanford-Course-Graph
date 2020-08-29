const express = require('express');
const path = require('path');
const fs = require('fs');


const graph = fs.readFileSync('./graph.json');


const app = express();

app.use(express.static(path.join(__dirname, '/')))

app.get('/graph', (req, res) => {
    res.send(JSON.parse(graph));
})

const port = process.env.PORT || 3000;
app.listen(port);