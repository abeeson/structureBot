#!/usr/bin/python3

import sys, requests
from requests.auth import HTTPBasicAuth

client_id = 'e29f9ccc16094478859fcc6a9767b836'
client_key = 'uE8lPf2zZwQrvAgAECNa9GfcFXwor4H8X6A0xUX0'

req = requests.post('https://login.eveonline.com/oauth/token', auth=HTTPBasicAuth(client_id,client_key), data={'grant_type':'authorization_code','code':sys.argv[1]})
if req.status_code == 200: print("Your refresh token is "+req.json()["refresh_token"])
if not req.status_code == 200: print(req.json())
