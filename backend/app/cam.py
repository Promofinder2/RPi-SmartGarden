import cv2
import time
from asyncore import read
import threading
import time

from cv2 import ROTATE_90_COUNTERCLOCKWISE
time.sleep(2)
import sys
sys.path.append('/home/pi/github-Projects/RPi-SmartGarden/RPi-SmartGarden/backend/')
import dash
from fastapi import Depends
from sqlalchemy.orm.session import Session
from dash.dependencies import Input, Output
from dash import dcc,html
import importlib
import flask
import pandas as pd
import os
import plotly as plt
import plotly.express as px
from database import db_DS18B20
from database.models import database_DS18B20,database_HTU21D
import cv2
from database.db import get_db
from routers import DS18B20
import asyncio
from quart import Quart, websocket
from typing import List
import base64
import threading
from dash_extensions import WebSocket
global cap
global ret
global img
delay_between_frames=0.05
server = Quart(__name__)

@server.websocket("/stream")
async def stream_capture():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
    while True:
        try:
            if delay_between_frames is not None:
                await asyncio.sleep(delay=delay_between_frames)
            frame = cap.get_frame()
            await websocket.send(f"data:image/jpeg;base64, {base64.b64encode(frame).decode()}")
        except AssertionError as e:
            print(e)


def take_10_pics():
        
    cap = cv2.VideoCapture(0)

    if cap.isOpened():
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    #    print('\n',f'CAP_PROP_FRAME_WIDTH\t{width}',f'CAP_PROP_FRAME_HEIGHT\t{height}',f'CAP_PROP_FRAME_FPS\t{fps}',f'CAP_PROP_FRAME_FRAME_COUNT\t{frame_count}')

    cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)
    cap.set(cv2.CAP_PROP_FPS,30)
    #start=time.time()
    x=0
    while True:
        x+=1
        try:
            num = len(os.listdir('/home/pi/github-Projects/RPi-SmartGarden/RPi-SmartGarden/backend/app/assets/'))
            ret,img = cap.read()
            if ret:
                rotate_image = cv2.rotate(img,rotateCode=ROTATE_90_COUNTERCLOCKWISE)
                gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                if x<80 and x >= 77:
                    time.sleep(20)
#                    cv2.imwrite(f'/home/pi/github-Projects/RPi-SmartGarden/RPi-SmartGarden/backend/app/assets/test_img{x}.jpg',img)
                    cv2.imwrite(f'/home/pi/github-Projects/RPi-SmartGarden/RPi-SmartGarden/backend/app/assets/test_portrait_{num}.jpg',rotate_image)
            if cv2.waitKey(1) == ord('q'):
                break
        except AssertionError as e:
            print(e)
        if x > 80:
            break
    cap.release()
    cv2.destroyAllWindows()


def main():
    while True:
        x=0
        if x < 48:
            take_10_pics()
            time.sleep(60*30)
        print(f'{x} photos have been taken')
        x+=1
        if x >=48:
            break

if __name__ == '__main__':
    main()