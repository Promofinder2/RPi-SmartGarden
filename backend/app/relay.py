import time
import RPi.GPIO as GPIO
import os


GPIO.setmode(GPIO.BOARD)
GPIO.setup(37,GPIO.OUT)
GPIO.setup(38,GPIO.OUT)
GPIO.setup(40,GPIO.OUT)

GPIO.output(38,True)
GPIO.output(38,False)
GPIO.cleanup()

