#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from database import Database

class Notification:
    def __init__(self):
        with open('./config.json','r') as config_file:
            config = json.load(config_file)
            NOTIFICATION = config["NOTIFICATION"]
            self.web_hook_url = NOTIFICATION["web_hook_url"]
            self.username = NOTIFICATION["username"]
            self.token = NOTIFICATION["token"]
            self.channel = NOTIFICATION["channel"]
            
            SCRAPING = config["SCRAPING"]
            self.country_code = ''.join(SCRAPING["country_code"])
            
            FLASK = config["FLASK"]
            self.access_link = FLASK["access_link"]
        self.db = Database()
        
    def do(self):
        """Slackへ通知
        """
        
        message = self.db.select_trading_result()
        files = {'file': open("./figure/graph.png", 'rb')}
        params = {
            "token":self.token,
            "channels":self.channel,
            #"filename":"gragh.png",
            "initial_comment": message
            #"title":"this is title"
            }
        r = requests.post('https://slack.com/api/files.upload',
                          params=params,
                          files=files)
        print(r.json())
        """
        requests.post(self.web_hook_url,data=json.dumps({
            "text" : message,
            "username" : self.username
            }), files = files)
        """
        return r