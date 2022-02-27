#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from flask import g
from webserver import Web
from scraping import Scraping
import csv
import os

class Database:
    def __init__(self):
        with open('./config.json','r') as config_file:
            config = json.load(config_file)
            SCRAPING = config["SCRAPING"]
            self.table_name = '_'.join(SCRAPING["country_code"])
            DATABASE = config["DATABASE"]
            self.data_quality = DATABASE["data_quality"]
            SCHEDULER = config["SCHEDULER"]
            self.triger_time = SCHEDULER["triger_time"]
        self.scr = Scraping()
        self.web = Web()
        with self.web.get_db() as con:
            cur = con.cursor()
            cur.execute("create table if not exists %s (runs interger, id interger, date integer, time integer, bid real, ask real)" % self.table_name)
            cur.execute("select MAX(runs) from %s" % self.table_name)
            for row in cur:
                if row[0] == None:
                    self.runs = 1
                    self.first_id = 1
                else:
                    self.runs = row[0] + 1
                    self.first_id = 1

    def data_insert(self):
        """DBへデータ追加
        """
        #スクレイピングによりデータ取得
        data_list = self.scr.get_data()
        
        with self.web.get_db() as con:
            cur = con.cursor()
            cur = con.execute("select max(id) from %s where runs = %d" % (self.table_name, self.runs)) 
            global id
            for row in cur:
                if row[0] == None:
                    id = 1
                else:
                    id = row[0] + 1
            data_list[0:0] = [self.runs, id]
            cur.execute('insert into %s values(?,?,?,?,?,?)' % self.table_name ,(data_list))
            con.commit()
        
    def data_select(self):
        """DBよりデータを取得

        Returns:
            _type_: _description_
        """
        with self.web.get_db() as con:
            cur = con.cursor()
            cur.execute("select id,date,time,bid,ask from %s where runs = %d order by date,time limit %d" % (self.table_name, self.runs, self.data_quality))
            data = cur.fetchall()
        
        return data
    
    def select_trading_result(self):
        with self.web.get_db() as con:
            cur = con.cursor()
            ask_data = cur.execute("select id,date,time,max(ask) from %s where runs = %d limit %d" % (self.table_name, self.runs, self.data_quality))
            for row in ask_data:
                max_ask_list = row
            search_range = id - max_ask_list[0]
            bid_data = cur.execute("select date,time,min(bid) from %s where runs = %d and id < %d and id >= %d " % (self.table_name, self.runs, self.data_quality, search_range))
            for row in bid_data:
                min_bid_list = row
        minutes = int(self.triger_time * self.data_quality / 60)
        chart_title = self.scr.get_chart_title()
        currency_name = chart_title.split('/')[1]
        message = '為替{}速報\n'.format(chart_title)
        if len(bid_data.fetchall()) == 0:
            profit = max_ask_list[3] - min_bid_list[2]
            purchasing_time = min_bid_list[1]
            selling_time = max_ask_list[2]
            message += '{}に買って、{}に売れば、{}の儲けでした。'.format(purchasing_time, selling_time, str(profit) + currency_name)
        else:
            message += '過去{}分以内では利益は出ませんでした。'.format(minutes)
        return message
    
    def update_csv(self):
        """終了時にcsv作成
        """
        print('Exit Flask\nUpdating CSV...')
        with self.web.get_db() as con:
            cur = con.cursor()
            cur.execute('select * from %s' % self.table_name)
            with open('./csv/' + self.table_name + '.csv', "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter="\t")
                csv_writer.writerow([i[0] for i in cur.description])
                csv_writer.writerows(cur)
        dirpath = os.getcwd() + "./csv/{}.csv".format(self.table_name)
        print("Data exported Successfully into {}".format(dirpath))