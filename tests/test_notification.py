from notification import Notification
import json

notify = Notification()


def test_do():
    
    assert notify.do().status_code == 200
    #assert ('OK' in notify.do().json()) == True