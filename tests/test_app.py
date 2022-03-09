from app import app


def test_database():
    app.config['TESTING'] = True
    client = app.test_client() 
    result = client.get('/database')
    assert result.status_code == 200
    assert (b'BID' in result.data) == True    

def test_index():
    app.config['TESTING'] = True
    client = app.test_client() 
    result = client.get('/')
    assert result.status_code == 200
    assert (b'Plot' in result.data) == True 

def test_plot():
    app.config['TESTING'] = True
    client = app.test_client() 
    result = client.get('/plot.png')
    assert result.status_code == 200
    assert isinstance(result.data, bytes) == True