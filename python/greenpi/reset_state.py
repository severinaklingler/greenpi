import RPi.GPIO as GPIO            # import RPi.GPIO module  
from time import sleep  

GPIO.setmode(GPIO.BCM)  

GPIO.setup(22, GPIO.OUT)
GPIO.output(22, 0) 