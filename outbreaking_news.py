import sqlite3
import json
import os
import matplotlib
import requests

#create database
print(requests.get('https://api.covid19api.com/').text)
# curl --location --request GET 'https://api.covid19api.com/'


#COVID API = use GET Day One
#Steam API = use GetRecentlyPlayedGames (v0001) http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key=XXXXXXXXXXXXXXXXX&steamid=76561197960434622&format=json