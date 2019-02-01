#!/usr/bin/python3

import configparser
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime

client_id = 'e29f9ccc16094478859fcc6a9767b836'
client_key = 'uE8lPf2zZwQrvAgAECNa9GfcFXwor4H8X6A0xUX0'

moons = {}
systems = {}
types = {}

config = configparser.ConfigParser()
config.read("structureBot.config")

refresh_token = config.get("config","refresh_token")
corp_id = config.get("config","corporation_id")

def refresh_esi_token():
  req = requests.post('https://login.eveonline.com/oauth/token', auth=HTTPBasicAuth(client_id,client_key), data={'grant_type':'refresh_token','refresh_token':refresh_token})
  if req.status_code == 200: return req.json()["access_token"]

def get_datetime_obj(datestring):
  dt = datetime.strptime(datestring, "%Y-%m-%dT%H:%M:%SZ")
  return dt

def get_moon(id):
  global moons
  if id in moons: return moons[id]
  req = requests.get('https://esi.evetech.net/v1/universe/moons/'+str(id), headers=header)
  moons[id] = req.json()
  return req.json()

def get_type(id):
  global types
  if id in types: return types[id]
  req = requests.get('https://esi.evetech.net/v3/universe/types/'+str(id), headers=header)
  types[id] = req.json()
  return req.json()

def make_slack_call(message):
  slack_token = config.get("config","slack_token")
  slack_channel = config.get("config","slack_channel")
  slack_header = {"User-Agent":"structureBot: https://github.com/abeeson/structureBot","Authorization":"Bearer "+slack_token,"Content-Type":"application/json; charset=utf-8"}
  slack_obj = {"channel":slack_channel,"text":message,"as_user":"true"}
  print message
  req = requests.post('https://slack.com/api/chat.postMessage', headers=slack_header, json=slack_obj)
  if "error" in req.json(): print("Bot error:"+req.json()["error"]) 

access_token = refresh_esi_token()
header = {'User-Agent':'structureBot: github link here','Authorization':'Bearer '+access_token}
req = requests.get('https://esi.evetech.net/v3/corporations/'+str(corp_id)+'/structures/', headers=header)
for structure in req.json():
  if 'fuel_expires' in structure:
    struct = requests.get('https://esi.evetech.net/v2/universe/structures/'+str(structure["structure_id"]), headers=header)
    timediff = get_datetime_obj(structure["fuel_expires"])-datetime.utcnow()
#    print(structure["structure_id"])
    if "error" in struct.json():
      print("Problem getting details for "+str(structure["structure_id"])+"\n")
      continue
#    print(struct.json()["name"] + " has " + str(timediff.days) + " days and " + str(timediff.seconds) + " seconds of fuel left\n")
    if timediff.days == 0 and timediff.seconds >= 82800:
      make_slack_call("\""+struct.json()["name"]+"\": Has less than a day of fuel left")
    if timediff.days == 0 and timediff.seconds <= 18800:
      make_slack_call("\""+struct.json()["name"]+"\": Has less than 6 hours of fuel left")

req = requests.get('https://esi.evetech.net/v1/corporations/'+str(corp_id)+'/starbases/', headers=header)
for pos in req.json():
  rate = 40
  hours = 0
  moon = get_moon(pos["moon_id"])
  type = get_type(pos["type_id"])
  if "Medium" in type["name"]: rate = 20
  if "Small" in type["name"]: rate = 10
  details = requests.get('https://esi.evetech.net/v1/corporations/'+str(corp_id)+'/starbases/'+str(pos['starbase_id'])+'?system_id='+str(pos['system_id']), headers=header).json()
  for fuel in details["fuels"]:
    fuel_type = get_type(fuel["type_id"])
    if "Block" in fuel_type["name"]:
      hours = fuel["quantity"]/rate
  if hours == 24: make_slack_call("*"+moon["name"]+"*\n_"+type["name"]+"_ has 24 hours of fuel remaining")
  if hours > 0 and hours < 6:  make_slack_call("*"+moon["name"]+"*\n_"+type["name"]+"_ has less than 6 hours of fuel remaining")
