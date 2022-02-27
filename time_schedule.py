#!/usr/bin/env python
# -*- coding: utf-8 -*-

from apscheduler.schedulers.background import BackgroundScheduler
import json

#定期実行
class Scheduler:
    """定期実行
    """
    def __init__(self):
        with open('./config.json','r') as config_file:
            config = json.load(config_file)
            SCHEDULER = config["SCHEDULER"]
            self.count_triger = SCHEDULER["count_triger"]
            self.triger_time = SCHEDULER["triger_time"]

        self.schedule = BackgroundScheduler(daemon=True)
    
    def execute(self,target):
        """引数を定期実行

        Args:
            target (_type_): _description_
        """
        self.schedule.add_job(target,'interval',seconds = self.triger_time) 
        self.schedule.start()
    
    def notify(self,notify_app):
        """引数のアプリに通知を送る

        Args:
            notify_app (_type_): _description_
        """
        self.schedule.add_job(notify_app, 'interval',seconds = self.triger_time * self.count_triger)