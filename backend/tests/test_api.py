from fastapi.testclient import TestClient
from app.main import app
c=TestClient(app)
def test_health(): assert c.get('/health').json()['status']=='ok'
def test_current_is_labeled():
 d=c.get('/weather/current').json(); assert 'source' in d['data'] and 'freshness' in d
def test_chat_grounded():
 d=c.post('/chat',json={'message':'Will it rain?','language':'hi'}).json(); assert d['grounding']['llm'].startswith('template') and 'Pune' in d['answer']
def test_bad_location(): assert c.get('/weather/current?location=Delhi').status_code==404
