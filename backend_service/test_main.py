from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_generate_sample_audio():
  the_text = "this is a test"
  response = client.get(f"/generate_sample_audio?text={the_text}&lang=en")
  assert response.status_code == 200

def test_recognize_speech():
  file = {'file': open("rsc/en_male.wav", 'rb')}
  resp = client.post(url="/recognize_speech/?lang=en", files=file, timeout=15.0)
  assert resp.status_code == 200
  resp = resp.json()
  assert resp['msg'] == "Success!"

def test_get_score():
  gt_text = 'hello, my name is'
  pred_text = gt_text + ' Albert'
  response = client.get(f"/get_score/?ground_truth={gt_text}&answer={pred_text}&lang=en")
  assert response.status_code == 200
  response = response.json()
  assert response['msg'] == "Success!"

def test_home():
  response = client.get("/")
  assert response.status_code == 200
  response = response.json()
  assert response['msg'] == "The Backend Service of The Speech Trainer"