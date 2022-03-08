from scraping import Scraping
import datetime

scr = Scraping()

def test_get_chart_title():
    #assert scr.get_chart_title() == "ユーロ/円"
    assert ('/' in scr.get_chart_title()) == True
    
def test_get_data():
    #mocker.patch.object(scr, ("date","time","bid","ask"))
    test_data = scr.get_data()
    #return全体
    assert len(test_data) == 3
    assert isinstance(test_data, list) == True
    
    #list[0]
    time_difference = datetime.datetime.now() - test_data[0]
    assert time_difference.seconds <= 1
    assert isinstance(test_data[0], datetime.datetime) == True
    #assert [0.5] <= scr.get_data()[1] - datetime.datetime.now().time()
    #list[2]
    assert isinstance(test_data[1], float) == True
    assert scr.get_data()[1] >= 0
    #list[3]
    assert isinstance(test_data[2], float) == True
    assert scr.get_data()[2] >= 0