# code from 'Pocket workflow'
#
# https://github.com/altryne/pocket_alfred
#
import SimpleHTTPServer
import SocketServer
import logging
import os
import signal
import sys
import json
import pocket
import main
import alfred

logger=main.logger
logger.setLevel(logging.INFO)

# Server port
PORT = 8273

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def getAuthToken(self):
        config=main.config_data()
        try:
            code = config['pocket_request_code']
        except:
            logger.info("getAuthToken invalid code")
            sys.exit(0)

        logger.info("request code is" + code)
        req_data = json.dumps({
                    "consumer_key": pocket.CONSUMER_KEY, "code": code
                })
        logger.info("Trying to get auth token")
        try:
            resp_data = pocket.makeRequest(req_data, pocket.POCKET_API_URL + 'authorize/')
            logger.info('Token received! :'+ resp_data["access_token"])
            config['pocket_access_code']=resp_data["access_token"]
            with open(os.path.join(alfred.work(False), 'config.json'), 'w+') as myFile:
                myFile.write(json.dumps(config))
            logger.info("Logged in as "+ resp_data["username"])
        except Exception:
            logger.error("Could not login - something went wrong")
    
    def do_GET(self):
        print "do_GET"
        logger.info("received a connection")
        self.getAuthToken()
        logger.info('Stopping servers')
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        sys.stdout.write("Welcome!")
        httpd.socket.close()
        logger.info('Stopping servers 2')
        processes = os.popen("ps -eo pid,command | grep server.py | grep -v grep | awk '{print $1}'").read().splitlines()
        logger.info('Processes pids : '+ " ".join(processes))
        for pid in processes:
            logger.info('Trying to stop proccess with the id ' + pid)
            cmd = os.kill(int(pid),signal.SIGTERM)
            logger.info('Success shutting down proccess')

# Initialize server object
httpd = SocketServer.TCPServer(("", PORT), ServerHandler)
#print "serving at port", PORT
logger.info("Server started at %d"%PORT)
httpd.serve_forever()
