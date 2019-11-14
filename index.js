const fs = require('fs');
const child_process = require('child_process');

const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();

app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));
app.use(
    '/js',
    express.static(path.join(__dirname, 'node_modules', 'jquery', 'dist'))
  );


app.get('/', function(req, res){
  var out = 'Write number';
  res.render('index', { out : out });
});

app.get('/go', (req, res) => {
  var out = 'Write number';
  var workerProcess = child_process.exec('net.py ',function 
  (error, stdout, stderr) {
  
  if (error) {
  console.log(error.stack);
  console.log('Error code: '+error.code);
  console.log('Signal received: '+error.signal);
  }
//  console.log('stdout: ' + stdout);
//  console.log('stderr: ' + stderr);
  out = stdout;
  console.log(out)
  res.render('index', { out : out });
  });
 
//  workerProcess.on('exit', function (code) {
//  console.log('Child process exited with exit code '+code);
//  res.render('index', { out : out });
//  });       
  
});

app.listen(3000);

