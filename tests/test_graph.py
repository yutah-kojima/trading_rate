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
            (15, '2022-02-28 22:42:20', 90, 95),
            (16, '2022-02-28 22:40:50', 105, 113),
            (17, '2022-02-28 22:41:00', 95, 108),
            (18, '2022-02-28 22:41:10', 80, 85),
            (19, '2022-02-28 22:41:20', 80, 85),
            (20, '2022-02-28 22:41:30', 80, 88),
			(21, '2022-02-28 22:40:00', 100, 105),
            (22, '2022-02-28 22:40:10', 85, 88),
            (23, '2022-02-28 22:40:20', 90, 95),
            (24, '2022-02-28 22:40:30', 100, 110),
            (25, '2022-02-28 22:40:40', 110, 113),
            (26, '2022-02-28 22:40:50', 105, 113),
            (27, '2022-02-28 22:41:00', 95, 108),
            (28, '2022-02-28 22:41:10', 80, 85),
            (29, '2022-02-28 22:41:20', 80, 85),
            (30, '2022-02-28 22:41:30', 80, 88),
            (31, '2022-02-28 22:41:40', 90, 100),
            (32, '2022-02-28 22:41:50', 95, 102),
            (33, '2022-02-28 22:42:00', 105, 108),
            (34, '2022-02-28 22:42:10', 110, 115),
            (35, '2022-02-28 22:42:20', 90, 95),
            (36, '2022-02-28 22:40:50', 105, 113),
            (37, '2022-02-28 22:41:00', 95, 108),
            (38, '2022-02-28 22:41:10', 80, 85),
            (39, '2022-02-28 22:41:20', 80, 85),
            (40, '2022-02-28 22:41:30', 80, 88),
			(41, '2022-02-28 22:40:00', 100, 105),
            (42, '2022-02-28 22:40:10', 85, 88),
            (43, '2022-02-28 22:40:20', 90, 95),
            (44, '2022-02-28 22:40:30', 100, 110),
            (45, '2022-02-28 22:40:40', 110, 113),
            (46, '2022-02-28 22:40:50', 105, 113),
            (47, '2022-02-28 22:41:00', 95, 108),
            (48, '2022-02-28 22:41:10', 80, 85),
            (49, '2022-02-28 22:41:20', 80, 85),
            (50, '2022-02-28 22:41:30', 80, 88),
            (51, '2022-02-28 22:41:40', 90, 100),
            (52, '2022-02-28 22:41:50', 95, 102),
            (53, '2022-02-28 22:42:00', 105, 108),
            (54, '2022-02-28 22:42:10', 110, 115),
            (55, '2022-02-28 22:42:20', 90, 95),
            (56, '2022-02-28 22:40:50', 105, 113),
            (57, '2022-02-28 22:41:00', 95, 108),
            (58, '2022-02-28 22:41:10', 80, 85),
            (59, '2022-02-28 22:41:20', 80, 85),
            (60, '2022-02-28 22:41:30', 80, 88),

    ]
    assert isinstance(graph.plot(chart_title, data), bytes) == True
    
    #ファイルの作成日
    file_path = './figure/graph.png'
    create_time = os.path.getctime(file_path)
    time_difference = (datetime.now().replace(microsecond=0) - datetime.fromtimestamp(int(create_time)))
    assert time_difference.seconds <= 5
