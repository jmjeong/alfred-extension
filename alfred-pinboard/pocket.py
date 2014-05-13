import json
import logging
import urllib2
import main

CONSUMER_KEY = '24219-095f416c4d869236ab85e38f'
REDIRECT_URI = 'http://j.mp/1c4E6Q2'
POCKET_API_URL = 'https://getpocket.com/v3/oauth/'

def makeRequest(request_data, request_url):
    request_headers = {'Content-Type': 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}
    request = urllib2.Request(request_url, request_data, request_headers)
    response = urllib2.urlopen(request)
    data = json.load(response)
    return data

def getRequestCode():
    req_data = json.dumps({
        'consumer_key':CONSUMER_KEY, 'redirect_uri':REDIRECT_URI
        })
    resp_data = makeRequest(req_data, POCKET_API_URL+'request/')
    return resp_data


def addpocket(q):
    config=main.config_data()
    try:
        token=config['pocket_access_code']
    except KeyError:
        print "Please login first with pbauthpocket"
        sys.exit(0)

    req_data = {
        'consumer_key':CONSUMER_KEY,
        'access_token':token,
        'url':q
        }
    resp = makeRequest(json.dumps(req_data),'https://getpocket.com/v3/add/')
    if resp["status"] == 1:
        print "Succesfully posted to pocket"
    
