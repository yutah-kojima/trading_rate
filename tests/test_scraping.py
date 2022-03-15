from scraping import Scraping
from datetime import datetime, timezone, timedelta
import json

scr = Scraping()

def test_get_chart_title():
    #assert scr.get_chart_title() == "ユーロ/円"
    assert ('/' in scr.get_chart_title()) == True
    
def test_get_data():
    with open('./config.json','r') as config_file:
        config = json.load(config_file)
        SCRAPING = config["SCRAPING"]
        utc_add_tz = SCRAPING["utc_add_tz"]
    tz = timezone(timedelta(hours=utc_add_tz[0]), utc_add_tz[1])

    test_data = scr.get_data()
    #return全体
    assert len(test_data) == 3
    assert isinstance(test_data, list) == True
    
    #list[0]
    dt_now = datetime.now(tz).replace(microsecond=0, tzinfo=None)
    time_difference = dt_now - test_data[0]
    assert time_difference.seconds <= 1
    assert isinstance(test_data[0], datetime) == True
    #assert [0.5] <= scr.get_data()[1] - datetime.datetime.now().time()
    #list[2]
    assert isinstance(test_data[1], float) == True
    assert scr.get_data()[1] >= 0
    #list[3]
    assert isinstance(test_data[2], float) == True
    assert scr.get_data()[2] >= 0