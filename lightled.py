import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

RED = 2
GREEN = 3
BLUE = 4

pins = [RED, GREEN, BLUE]

def light_led(color):
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)
    GPIO.setup(color, GPIO.OUT)
    GPIO.output(color, 1)

def light_led_white():
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 1)       

def light_led_clear():
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, 0)   


while True:
    light_led_clear()

