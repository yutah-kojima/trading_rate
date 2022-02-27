#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, g
import sqlite3
import json
from scraping import Scraping

class Web:
    def __init__(self):
        with open('./config.json','r') as config_file:
            config = json.load(config_file)
            FLASK = config["FLASK"]
            self.db_path = FLASK["db_path"]
        self.scr = Scraping()
        self.app = Flask(__name__)
    
    def get_db(self):
        with self.app.app_context():
            if 'db' not in g:
                g.db = sqlite3.connect(self.db_path)
            return g.db

    def close_db(e=None):
        db = g.pop('db', None)
        if db is not None:
            db.close()

