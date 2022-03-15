#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from database import Database
from slack_sdk import WebClient
import os
from datetime import datetime
import time

class Notification:
    def __init__(self):
        with open('./config.json','r') as config_file:
            config = json.load(config_file)
            NOTIFICATION = config["NOTIFICATION"]
            self.username = NOTIFICATION["username"]
            self.token = NOTIFICATION["token"]
            self.channel = NOTIFICATION["channel"]
            
            SCRAPING = config["SCRAPING"]
            self.country_code = ''.join(SCRAPING["country_code"])
        
    def do(self):
        """Slackへ通知
        """
        db = Database()      
        client = WebClient(self.token)
        message = db.select_trading_result()        
        
        files = "./figure/graph.png"
        
        #ファイルの作成日
        while True:
            create_time = datetime.fromtimestamp(int(os.path.getctime(files)))
            time_difference = (datetime.now().replace(microsecond=0) - create_time)
            if time_difference.seconds <= 15:
                r = client.files_upload(channels = self.channel, file = files, initial_comment= message, filename="graph")
                break
            else:
                time.sleep(1)
        return r
    
