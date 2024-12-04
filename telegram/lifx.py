#!/usr/bin/python

'''
edited from mac
Send Json Data to Lifx URLs - See 2 URLs
https://api.lifx.com/v1/lights/
https://api.lifx.com/v1/lights/{0}/effects/pulse  - use Lamda PUT!!
data = {
		"power": "on",
		"color": "green saturation:0.5",
		"brightness": 0.2,
		"duration": 5
		}
'''
	
	
import json
import urllib.request
import os

lifxUrl = 'https://api.lifx.com/v1/lights/'
lifxToken = 'Bearer {0}'.format(os.environ["LIFX_APIKEY"])
def getState():
	#cmd = 'curl "{0}" -H "Authorization: Bearer {1}"'.format(lifxUrl,lifxToken)
	state = {}
	req = urllib.request.Request(lifxUrl)
	req.add_header('Authorization',lifxToken)
	response = urllib.request.urlopen(req)
	
	lifxBulbs = json.loads(response.read())
	
	for k,v in enumerate(lifxBulbs):
		state[v['label']]=[v['id'],v['power']]
	
	return state


def setEffects(bulbId,data):
	url = 'https://api.lifx.com/v1/lights/{0}/effects/pulse'.format(bulbId)
	req = urllib.request.Request(url)
	req.add_header('Content-Type', 'application/json')
	req.add_header('Authorization',lifxToken)
	response = urllib.request.urlopen(req,json.dumps(data).encode('utf-8'))
	response =  json.loads(response.read())
	return response



def setState(bulbId, data):
	
	url = 'https://api.lifx.com/v1/lights/{0}/state'.format(bulbId)
	req = urllib.request.Request(url)
	req.add_header('Content-Type', 'application/json')
	req.add_header('Authorization',lifxToken)
	req.get_method = lambda: 'PUT'
	response = urllib.request.urlopen(req,json.dumps(data).encode('utf-8'))
	response = json.loads(response.read())
	return response


