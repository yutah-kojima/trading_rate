#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import atexit

#Flask
from flask import Flask, render_template, make_response

#Database
from database import Database

#スクレイピング
from scraping import Scraping

#グラフ
from graph import Graph

#定期実行
from time_schedule import Scheduler

#通知
from notification import Notification


#setting
with open('./config.json','r') as config_file:
    config = json.load(config_file)
    FLASK = config["FLASK"]
    reflesh_interval = FLASK["reflesh_interval"]
    file_type = FLASK["file_type"]
    config_file.close()


#インスタンス作成
scr = Scraping()
db = Database()
graph = Graph()
schedule = Scheduler()
notify = Notification()


#定期実行
schedule.execute(db.data_insert)
#アプリ通知
schedule.notify(notify.do)

atexit.register(db.update_csv)

app = Flask(__name__)

@app.route('/database')
def database():
    chart_title = scr.get_chart_title()
    data = db.data_select()
    return render_template('db.html', reflesh_interval=reflesh_interval, chart_title=chart_title ,data=data)

@app.route('/')
def index():
    return render_template('plot.html', reflesh_interval=reflesh_interval)


@app.route('/plot.png')
def plot():
    data = db.data_select()
    chart_title = scr.get_chart_title()
    plot_data = graph.plot(chart_title,data)
    response = make_response(plot_data)
    response.headers['Content-Type'] = file_type
    response.headers['Content-Length'] = len(plot_data)
    return response



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
    