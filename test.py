import requests
import json
import time

start = time.time()
# resp = requests.post("https://getprediction-eb7wj7y6sa-as.a.run.app", files={'file': open('BAD1.jpg','rb')})
# resp = requests.post("https://getpredictml-eb7wj7y6sa-et.a.run.app", files={'file': open('CM1.JPG','rb')})
resp = requests.post("http://127.0.0.1:5000/", files={'file': open('BAD1.jpg','rb')})
end = time.time()
timer = end - start
# result = json.loads(resp)

print(resp.status_code)
print(resp.text)

print(timer)