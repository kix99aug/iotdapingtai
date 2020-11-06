from requests import Session
import random,time
s = Session()
s.headers = {"CK": "PK1A4T9GU1M23G57Y9"}

r = s.get("https://iot.cht.com.tw/iot/v1/device")

start = time.time()
for i in r.json():
    r = s.post("https://iot.cht.com.tw/iot/v1/device/%s/rawdata" % i['id'], json=[
        {
            "id": "cars",
            "save": True,
            "value": [20 + int(10*random.random()) - 5]
        },
        {
            "id": "speed",
            "save": True,
            "value": [100 + int(20*random.random()) - 10]
        }
    ]
    )
end = time.time()

print(end-start)
