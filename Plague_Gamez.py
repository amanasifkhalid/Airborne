import sqlite3
import json
import os
import matplotlib
import requests

#create database
print(requests.get('https://api.covid19api.com/').text)
# curl --location --request GET 'https://api.covid19api.com/'