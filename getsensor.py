from requests import Session
s = Session()
s.headers = {"CK": "PK1A4T9GU1M23G57Y9"}

r = s.get("https://iot.cht.com.tw/iot/v1/device")

for i in r.json():
    s.delete("https://iot.cht.com.tw/iot/v1/device/%s/sensor/%s/rawdata"%(i["id"],"cars"),params={
        "start":"2016-07-14T23:55:00Z",
        "end":"2020-11-06T23:55:00Z"
    })
    s.delete("https://iot.cht.com.tw/iot/v1/device/%s/sensor/%s/rawdata"%(i["id"],"speed"),params={
        "start":"2016-07-14T23:55:00Z",
        "end":"2020-11-06T23:55:00Z"
    })