#!/usr/bin/env python
# -*- coding: utf-8 -*-

from graph import Graph
import os
from datetime import datetime

def test_plot():
    graph = Graph()
    chart_title = 'test_title'
    data = [(1, '2022-02-28 22:40:00', 100, 105),
            (2, '2022-02-28 22:40:10', 85, 88),
            (3, '2022-02-28 22:40:20', 90, 95),
            (4, '2022-02-28 22:40:30', 100, 110),
            (5, '2022-02-28 22:40:40', 110, 113),
            (6, '2022-02-28 22:40:50', 105, 113),
            (7, '2022-02-28 22:41:00', 95, 108),
            (8, '2022-02-28 22:41:10', 80, 85),
            (9, '2022-02-28 22:41:20', 80, 85),
            (10, '2022-02-28 22:41:30', 80, 88),
            (11, '2022-02-28 22:41:40', 90, 100),
            (12, '2022-02-28 22:41:50', 95, 102),
            (13, '2022-02-28 22:42:00', 105, 108),
            (14, '2022-02-28 22:42:10', 110, 115),
            (15, '2022-02-28 22:42:20', 90, 95)
    ]
    assert isinstance(graph.plot(chart_title, data), bytes) == True
    
    #ファイルの作成日
    file_path = './figure/graph.png'
    create_time = os.path.getctime(file_path)
    assert datetime.fromtimestamp(int(create_time)) == datetime.now().replace(microsecond=0)