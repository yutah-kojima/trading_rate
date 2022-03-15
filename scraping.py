#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
import json

class Scraping:
    def __init__(self):
        with open('./config.json','r') as config_file:
            config = json.load(config_file)
            SCRAPING = config["SCRAPING"]
            self.country_code = ''.join(SCRAPING["country_code"])
            utc_add_tz = SCRAPING["utc_add_tz"]
        self.tz = timezone(timedelta(hours=utc_add_tz[0]), utc_add_tz[1])
        self.url = "https://info.finance.yahoo.co.jp/fx/detail/?code={}=FX".format(self.country_code)

    
    def get_chart_title(self):
        """チャートのタイトルを取得する。
        """
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content,'html.parser')
        chart_title = soup.select_one('#main > div.fxChartTtl > h1 > span').find_all(text=True)[0]
        return chart_title

        
    def get_data(self):
        """スクレイピング

        Returns:
            list: _description_
        """
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content,'html.parser')

        bid = float(''.join(soup.select_one('#{}_detail_bid'.format(self.country_code)).find_all(text=True)))
        ask = float(''.join(soup.select_one('#{}_detail_ask'.format(self.country_code)).find_all(text=True)))
    
        #日時取得
        dt = datetime.now(self.tz)
        dt = dt.replace(microsecond=0, tzinfo=None)

        data_list = [dt,bid,ask]        
        return data_list