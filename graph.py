#!/usr/bin/env python
# -*- coding: utf-8 -*-

import japanize_matplotlib
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

import json

class Graph:
    def __init__(self):
        with open('./config.json','r') as config_file:
            config = json.load(config_file)
            GRAPH = config["GRAPH"]
            self.number_scale = GRAPH["number_scale"]
            self.x_label_rotation = GRAPH["x_label_rotation"]
            self.picture_name = GRAPH["picture_name"]
            SCHEDULER = config["SCHEDULER"]
            self.count_triger = SCHEDULER["count_triger"]
        
    def plot(self, chart_title, data):
        """プロットデータ作成

        Args:
            country_name (_type_): _description_
            data (_type_): _description_

        Returns:
            _type_: _description_
        """
        id_for_plot = 0
        x = []
        y_bid = []
        y_ask = []
        for row in data:
            id_for_plot = row[0]
            x.append(row[2])
            y_bid.append(row[3])
            y_ask.append(row[4])
        fig, ax = plt.subplots()
        ax.set_title(chart_title)   
        ax.plot(x,y_bid,label='Bid(売値)')
        ax.plot(x,y_ask,label='Ask(買値)')
        ax.grid(which='both')
        ax.legend()
        if id_for_plot % self.count_triger == 0:
            plt.savefig('./figure/{}.png'.format(self.picture_name))
        self.adjust_x_space(x,ax)
        canvas = FigureCanvasAgg(fig)
        png_output = BytesIO()
        canvas.print_png(png_output)
        plot_data = png_output.getvalue()
        plt.close()
        return plot_data
        
    def adjust_x_space(self,x,ax):
        """x軸の間隔調整
        """
        x_cnt = len(x)
        if x_cnt >= self.number_scale:
            x_interval = x_cnt / self.number_scale
            ax.set_xticks(np.arange(0, x_cnt, step=x_interval))
            ax.tick_params(axis='x', rotation=self.x_label_rotation)