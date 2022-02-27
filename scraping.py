#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import datetime
import json

class Scraping:
    def __init__(self):
        with open('./config.json','r') as config_file:
            config = json.load(config_file)
            SCRAPING = config["SCRAPING"]
            self.country_code = ''.join(SCRAPING["country_code"])
            self.url = SCRAPING["url"].format(self.country_code)
        
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

        bid = ''.join(soup.select_one('#{}_detail_bid'.format(self.country_code)).find_all(text=True))
        ask = ''.join(soup.select_one('#{}_detail_ask'.format(self.country_code)).find_all(text=True))
    
        #日時取得
        date = datetime.date.today()
        time = datetime.datetime.now().time()
    
        data_list = [date.strftime('%Y-%m-%d'),time.strftime('%H:%M:%S'),bid,ask]
        
        return data_list