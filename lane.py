import random,time,sys
from requests import Session
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
from celluloid import Camera
s = Session()
s.headers = {"CK": "PK1A4T9GU1M23G57Y9"}

# 兩秒一台車
# 時速90~110
# 遇到前車的話速度相同
# 反應+煞停時間 4秒 煞停距離 50m

class Car:
    def __init__(self,bomb):
        self.speed = 90 + int(20*random.random())
        self.basespeed = self.speed
        self.pos = 0
        self.safedis = 50+ int(100*random.random())
        self.crash = False
        self.bomb = bomb
    def drive(self,front_pos,front_speed):
        previous_pos = self.pos
        if self.crash: return (int(previous_pos/10),int(self.pos/10))
        if (self.bomb and self.pos > 1000): front_pos = 10+self.safedis + self.pos
        if(self.pos + self.speed / 3600 * 1000 + self.safedis > front_pos):
            minusspeed = (front_pos-self.safedis - self.pos) *3600 / 1000
            if(minusspeed > 25):
                if self.speed - minusspeed >= 0 : self.speed -= 25
                else: self.speed = 0
            else: self.speed -= minusspeed
        else:
            if(self.speed<self.basespeed): self.speed += 2
        self.pos = self.pos + self.speed / 3600 * 1000
        if(self.pos > front_pos):
            self.crash = True
            self.speed = 0
            self.pos = front_pos 
        return (int(previous_pos/10),int(self.pos/10)+1)
    pass

class Sensor:
    def __init__(self,id):
        self.id = id
        self.cars = 0
        self.speedsum = 0
    def post(self):
        r = s.post("https://iot.cht.com.tw/iot/v1/device/%s/rawdata" % self.id, json=[
        {
            "id": "cars",
            "save": True,
            "value": [self.cars]
        },
        {
            "id": "speed",
            "save": True,
            "value": [self.speedsum / self.cars]
        }
        ])
        self.cars = 0
        self.speedsum = 0

cars = []
sensors = []

i = 0
r = s.get("https://iot.cht.com.tw/iot/v1/device")
for sensor in r.json():
    sensors.append(Sensor(sensor['id']))
while True:
    if i%5 == 0 and i < 60 :
        if i == 30: cars.append(Car(True))
        else :cars.append(Car(False))
    i+=1
    previous_pos = sys.maxsize
    previous_speed = sys.maxsize
    x = []
    y = []
    lim = 0
    for c in cars:
        (f,t) = c.drive(previous_pos,previous_speed)
        previous_pos = c.pos
        previous_speed = c.speed
        for j in range(f,t):
            if j >= len(sensors):
                cars.remove(c)
                break
            sensors[j].cars += 1
            sensors[j].speedsum += c.speed
        x.append(c.pos)
        y.append(1)
        if lim==0 : lim = c.pos
    plt.cla()
    plt.scatter(x,y)
    plt.xlim(0,2000)
    plt.savefig("fig/%d.jpg"%i)
            
    # time.sleep(0.01)
    if i%10 == 0:
        for sensor in sensors:
            if sensor.cars != 0: 
                sensor.post()
                pass