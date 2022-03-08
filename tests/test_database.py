#!/usr/bin/env python
# -*- coding: utf-8 -*-

from database import Database
from flask import g
import json
from datetime import datetime
import os

"""
@pytest.fixture
def setup(mocker, temp_dbfile):
    mocker.patch.object(db, 'runs', test_max_runs)
    #mocker.patch(db.select_trading_result().new_id, 'new_id', test_id)
    #mocker.patch.object(db, 'table_name', "test")
    #mocker.patch.object(web, "get_db", temp_dbfile)
    #mocker.patch.object(web, 'db_path', temp_dbfile.name)


test_max_runs = 1
test_id = 7
new_id = 6
#db.select_trading_result().new_id = test_id
"""
def test_get_db():
    with open('./config.json','r') as config_file:
        config = json.load(config_file)
        SCRAPING = config["SCRAPING"]
        table_name = '_'.join(SCRAPING["country_code"])
    db = Database()
    with db.get_db() as con:
        cur = con.cursor()
        cur.execute("SELECT MAX(datetime) FROM %s" % table_name)
        for row in cur:
            #データベースが開いているかどうかを確認
            assert isinstance(row, tuple) == True

def test_data_insert():
    with open('./config.json','r') as config_file:
        config = json.load(config_file)
        SCRAPING = config["SCRAPING"]
        table_name = '_'.join(SCRAPING["country_code"])
    db = Database()
    db.data_insert()
    with db.get_db() as con:
        cur = con.cursor()
        cur.execute("SELECT runs, MAX(datetime) FROM %s" % table_name)
        for row in cur:
            time_difference = datetime.now().replace(microsecond=0) - datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
            test_runs = row[0]
            assert time_difference.seconds <= 1
        #後処理(入力データ削除)
        cur.execute("DELETE FROM %s WHERE runs = %s" % (table_name,test_runs))
        con.commit()

def test_select_trading_result():
    db = Database()
    assert ("為替" in db.select_trading_result()) == True

def test_update_csv():
    with open('./config.json','r') as config_file:
        config = json.load(config_file)
        SCRAPING = config["SCRAPING"]
        table_name = '_'.join(SCRAPING["country_code"])
    db = Database()
    db.update_csv()
    csv_path = './csv/{}.csv'.format(table_name)
    update_time = os.path.getmtime(csv_path)
    assert datetime.fromtimestamp(int(update_time)) == datetime.now().replace(microsecond=0)