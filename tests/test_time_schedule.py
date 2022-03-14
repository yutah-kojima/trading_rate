#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time_schedule import Scheduler
import json
from datetime import datetime,timedelta
from apscheduler.schedulers.background import BackgroundScheduler


def t_func():
    return ("testing")


def test_execute():
    with open('./config.json','r') as config_file:
        config = json.load(config_file)
        SCHEDULER = config["SCHEDULER"]
        count_triger = SCHEDULER["count_triger"]
        triger_time = SCHEDULER["triger_time"]
    sched = Scheduler()    
    sched.execute(t_func)
    scheduler = BackgroundScheduler()
    for job in scheduler.get_jobs():
        #if name != 'name of job you care about':
            #continue

        assert job.next_run_time >= datetime.utcnow() + timedelta(seconds = triger_time * count_triger - 1)
        assert job.next_run_time <= datetime.utcnow() + timedelta(seconds = triger_time * count_triger + 1)

def test_notify():
    with open('./config.json','r') as config_file:
        config = json.load(config_file)
        SCHEDULER = config["SCHEDULER"]
        count_triger = SCHEDULER["count_triger"]
        triger_time = SCHEDULER["triger_time"]

    sched = Scheduler()
    sched.notify(t_func)
    scheduler = BackgroundScheduler()
    
    for job in scheduler.get_jobs():
        #if name != 'name of job you care about':
            #continue

        assert job.next_run_time >= datetime.utcnow() + timedelta(seconds = triger_time * count_triger - 1)
        assert job.next_run_time <= datetime.utcnow() + timedelta(seconds = triger_time * count_triger + 1)