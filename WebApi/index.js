const express = require('express');
const getNextDeparture = require('./src/DataProvider/nextDepartureProvider')
const app = express();
const port = 3111;

app.get('/transit/next_departure', (req, res) => res.send(JSON.stringify(getNextDeparture())));

app.listen(
    port, 
    () => console.log(`Example app listening on port ${port}!`));