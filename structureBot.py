#!/usr/bin/python

import ConfigParser
import requests
from requests.auth import HTTPBasicAuth

client_id = 'e29f9ccc16094478859fcc6a9767b836'
client_key = 'uE8lPf2zZwQrvAgAECNa9GfcFXwor4H8X6A0xUX0'

config = ConfigParser.ConfigParser()
config.read("structureBot.config")

refresh_token = config.get("config","refresh_token")

def refresh_esi_token():
  req = requests.post('https://login.eveonline.com/oauth/token', auth=HTTPBasicAuth(client_id,client_key), data={'grant_type':'refresh_token','refresh_token':refresh_token})
  if req.status_code == 200: return req.json()["access_token"]

access_token = refresh_esi_token()
header = {'User-Agent':'structureBot: github link here','Authorization':'Bearer '+access_token}
req = requests.get('https://esi.evetech.net/v2/corporations/98088408/structures/', headers=header)
for structure in req.json():
  if 'fuel_expires' in structure:
    struct = requests.get('https://esi.evetech.net/v1/universe/structures/'+str(structure["structure_id"]), headers=header)
    print "\""+struct.json()["name"]+"\": fuel expires at "+structure["fuel_expires"]
