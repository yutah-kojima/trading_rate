#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import Flask, g
import sqlite3
import csv
import os
from scraping import Scraping
from decimal import Decimal

class Database:
    def __init__(self):
        with open('./config.json','r') as config_file:
            config = json.load(config_file)
            SCRAPING = config["SCRAPING"]
            self.table_name = '_'.join(SCRAPING["country_code"])
            DATABASE = config["DATABASE"]
            self.data_quality = DATABASE["data_quality"]
            self.db_path = DATABASE["db_path"]
            SCHEDULER = config["SCHEDULER"]
            self.triger_time = SCHEDULER["triger_time"]
        self.app = Flask(__name__)
        self.scr = Scraping()
        with self.get_db() as con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS %s (runs INTEGER, id INTEGER, datetime DATETIME, bid REAL, ask REAL);" % self.table_name)
            #新しいrunsを取得
            cur.execute("SELECT MAX(runs) FROM %s" % self.table_name)
            for row in cur:
                if row[0] == None:
                    self.runs = 1
                else:
                    self.runs = row[0] + 1
        
    def get_db(self):
        with self.app.app_context():
            if 'DB' not in g:
                g.DB = sqlite3.connect(self.db_path,detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
            # "TIMESTAMP"コンバータ関数 をそのまま ”DATETIME” にも使う
            sqlite3.dbapi2.converters['DATETIME'] = sqlite3.dbapi2.converters['TIMESTAMP']
            return g.DB
    
    """
    def close_db(e=None):
        DB = g.pop('DB', None)
        if DB is not None:
            DB.close()
    """
            
    def data_insert(self):
        """DBへデータ追加
        """
        #スクレイピングによりデータ取得
        data_list = self.scr.get_data()
        
        with self.get_db() as con:
            cur = con.cursor()
            cur = con.execute("SELECT runs, MAX(id) FROM %s WHERE runs = %d" % (self.table_name, self.runs)) 
            for row in cur:
                if row[1] == None:
                    new_id = 1
                else:
                    new_id = row[1] + 1
            data_list[0:0] = [self.runs, new_id]
            cur.execute('insert into %s values(?,?,?,?,?)' % self.table_name ,(data_list))
            con.commit()
        
    def data_select(self):
        """DBよりデータを取得

        Returns:
            _type_: _description_
        """
        with self.get_db() as con:
            cur = con.cursor()
            cur.execute("SELECT id, datetime, bid, ask FROM %s WHERE runs = %d ORDER BY datetime LIMIT %d" % (self.table_name, self.runs, self.data_quality))
            data = cur.fetchall()
        
        return data
    
    def select_trading_result(self):
        with self.get_db() as con:
            cur = con.cursor()
            #現在のruns取得
            cur.execute("SELECT MAX(runs) FROM %s" % self.table_name)
            for row in cur:
                current_runs = row[0]
            #最新のidを取得
            cur.execute("SELECT MAX(id) FROM %s WHERE runs = %d LIMIT %d" % (self.table_name, current_runs, self.data_quality))
            for row in cur:
                last_id = row
            #最大の売値を取得
            cur.execute("SELECT id, datetime, MAX(bid) FROM %s WHERE runs = %d LIMIT %d" % (self.table_name, current_runs, self.data_quality))
            for row in cur:
                max_bid_list = row
            start_id = last_id[0] - self.data_quality +1
            cur.execute("SELECT datetime, MIN(ask) FROM %s WHERE runs = %d AND id >= %d AND id < %d" % (self.table_name, current_runs, start_id, max_bid_list[0]))
            for row in cur:
                min_ask_list = row
        minutes = int(self.triger_time * self.data_quality / 60)
        chart_title = self.scr.get_chart_title()
        currency_name = chart_title.split('/')[1]
        message = '為替{}速報\n'.format(chart_title)
        if isinstance(min_ask_list, float) == True:
            #浮動小数の計算
            profit =  Decimal(str(max_bid_list[2])) - Decimal(str(min_ask_list[1]))
            purchasing_time = min_ask_list[0].time()
            selling_time = max_bid_list[1].time()
            message += '{}に買って、{}に売れば、{}の儲けでした。'.format(purchasing_time, selling_time, str(profit) + currency_name)
        else:
            message += '過去{}分以内では利益は出ませんでした。'.format(minutes)
        print(message)
        
        return message
    
    def update_csv(self):
        """終了時にcsv作成
        """
        print('Exit Flask\nUpdating CSV...')
        with self.get_db() as con:
            cur = con.cursor()
            cur.execute('select * from %s' % self.table_name)
            with open('./csv/' + self.table_name + '.csv', "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter="\t")
                csv_writer.writerow([i[0] for i in cur.description])
                csv_writer.writerows(cur)
        dirpath = os.getcwd() + "./csv/{}.csv".format(self.table_name)
        print("Data exported Successfully into {}".format(dirpath))