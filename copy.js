const http = require('http');
const { exec } = require('child_process');
const fs = require('fs');

//create a server object:
http.createServer(function (req, res) {

  //if the request url is: localhost:8080
  if(req.url === "/"){
    fs.readFile("NumReader/vueNumR/index.html", function(err, data){
      res.writeHead(200, {'Content-Type': 'text/html'});
      res.write(data);
      res.end();
    });
  //if the request url is: localhost:8080/run
  }else if(req.url === "/run"){


    exec('./ /NumReader/net.py', (error, stdout, stderr) => {
     if (error) {
       console.error(error.stack);
       res.write('Command has failed'); //write a response to the client
       res.end(); //end the response
       return;
     }
     console.log('stdout: ${stdout}');
     console.log('stderr: ${stderr}');

     res.write('Command has been run'); //write a response to the client
     res.end(); //end the response
    });
  }

}).listen(8080); //the server object listens on port 8080



#example{padding:0px 0px 0px 100px;display:none;}
#example .new{opacity: 0;}
#example .div_opacity{
  -webkit-transition: opacity .1s ease-in-out;
  -moz-transition: opacity .1s ease-in-out;
  -ms-transition: opacity .1s ease-in-out;
  -o-transition: opacity .1s ease-in-out;
  transition: opacity .1s ease-in-out;
  opacity: 1;}
  

  <div class="welcome-bg" v-if="popups.showWelcome">
  <div class="welcome">
      <h1 class="fade-up">NumReader</h1>
      <h2 class="fade-up">
          By Sergey Chernetsov
      </h2>
      <a href="//twitter.com/lewitje" target="blank" title="Lewi Hussey on Twitter" class="fade-up">@sergerey</a>
      <span class="btn fade-up"
                  title="Close"
                  v-on:click="popups.showWelcome = false">
          Lets go
      </span>
  </div>
</div>