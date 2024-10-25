import RPi.GPIO as GPIO
import time

rel_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(rel_pin, GPIO.OUT)
GPIO.output(rel_pin, GPIO.LOW)  # 默认关闭继电器

def open_door():
    GPIO.output(rel_pin, GPIO.HIGH)
    print("Door opened")
    time.sleep(5)
    GPIO.output(rel_pin, GPIO.LOW)
    print("Door closed")

def cleanup():
    GPIO.cleanup()
