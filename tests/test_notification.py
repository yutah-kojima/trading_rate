from notification import Notification
import json

notify = Notification()


def test_do():
    
    assert ('OK' in notify.do().json()) == True