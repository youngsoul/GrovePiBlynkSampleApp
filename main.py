from grovepi import grovepi
from pyblynkrestapi.PyBlynkRestApi import PyBlynkRestApi
import time
import grove_rgb_lcd
import threading

"""
Sample application to show an integration between the
Raspberry PI, GrovePI+ board and sensors, and the Blynk
Cloud and mobile application using the Python library
PyBlynkRestApi

The example assumes the following sensors:

D6 - Button - V20
D3 - LED 1 - V21
D5 - LED 2 - V22
D2 - RGB LED - V30,V31,V32

I2C - RGB LCD
I2C - 3 Axis

A0 - Rotary Switch 1 - V23
A1 - Rotary Switch 2 - V24
A2 - Light Sensor - V25

When Button is pressed, turn on the LED on the Blynk App

When a momentary Blynk button is pressed, turn on LED 1

When a switch Blynk button is pressed, turn on LED 2

Using the Blynk zeRGBa component, set the value of the RGB LED

When Rotary switch 1 is changed, update a Blynk gauge

When Rotary switch 2 is changed, update a Blynk gauge

Using light Sensor update a Blynk Graph

Using 3Axis, update x,y,z value in Blynk Value display




"""

button = 6
led1 = 3
led2 = 5
rgb_led = 2

rotary1 = 0
rotary2 = 1
light = 2

# Only a single thread can access the grovepi api at a time
# and since the PyBlynk library is multiple threaded, we
# have to create a semaphore around the grovepi api to
# insure that only a single thread accesses the api
grovepi_semaphore = threading.Semaphore()

def init():
    grovepi.pinMode(button, 'INPUT')
    grovepi.pinMode(led1, 'OUTPUT')
    grovepi.pinMode(led2, 'OUTPUT')
    grovepi.pinMode(rgb_led, 'OUTPUT')

    grovepi.chainableRgbLed_init(rgb_led, 1)

    with open('./auth_token.txt', 'r') as f:
        auth_token = f.readline().strip()

    return PyBlynkRestApi(auth_token=auth_token, start_heartbeat=True)


def read_rotary1_handler(blynk_pin_number, blynk):
    with grovepi_semaphore:
        value = grovepi.analogRead(rotary1)

    adjusted_value = int((value*100)/1024)
    return adjusted_value

def read_rotary2_handler(blynk_pin_number, blynk):
    with grovepi_semaphore:
        value = grovepi.analogRead(rotary2)
    adjusted_value = int((value*100)/1024)
    return adjusted_value

def read_light_handler(blynk_pin_number, blynk):
    with grovepi_semaphore:
        sensor_value = grovepi.analogRead(light)
    # Calculate resistance of sensor in K
    #resistance = (float)(1023 - sensor_value) * 10 / sensor_value
    adjusted_value = int(sensor_value)
    print("{} | {}".format(sensor_value, adjusted_value))
    return adjusted_value

def read_button_handler(blynk_pin_number, blynk):
    """
    Read Button and return the button value.
    :param blynk:
    :return:
    """
    with grovepi_semaphore:
        button_value = grovepi.digitalRead(button)
    return button_value*255

def set_slider_to_lcd_handler(value, blynk_pin_number, blynk):
    """
    Read Button and return the button value.
    :param blynk:
    :return:
    """
    grove_rgb_lcd.setRGB(255,0,255)
    grove_rgb_lcd.setText("Slider Value:{}".format(value))

    return

def set_rgb_led_handler(blynk):
    # read the rgb value
    # you just need to read one of the rgb values
    # and the return is all three
    rgb_values = blynk.get_pin_value('V30')

    r = int(rgb_values[0] if rgb_values[0] != '' else 0)
    g = int(rgb_values[1] if rgb_values[1] != '' else 0)
    b = int(rgb_values[2] if rgb_values[2] != '' else 0)

    print("rgb: {}:{}:{}".format(r,g,b))
    with grovepi_semaphore:
        grovepi.storeColor(r,g,b)
        grovepi.chainableRgbLed_pattern(rgb_led, 0, 0)


def set_acc_handler(blynk):
    with grovepi_semaphore:
        values = grovepi.acc_xyz()
    print("{}".format(values))
    blynk.set_pin_value('V27', "{}".format(values[0]))
    blynk.set_pin_value('V28', "{}".format(values[1]))
    blynk.set_pin_value('V29', "{}".format(values[2]))

def set_led1_handler(value, blynk_pin_number, blynk):
    if value == '':
        value = 0
    with grovepi_semaphore:
        grovepi.digitalWrite(led1, int(value))
    return

def set_led2_handler(value, blynk_pin_number, blynk):
    if value == '':
        value = 0
    with grovepi_semaphore:
        grovepi.digitalWrite(led2, int(value))
    return

if __name__ == '__main__':
    blynk = init()
    blynk.add_set_pin_handler('V20', read_button_handler)
    blynk.add_read_pin_handler('V21', set_led1_handler)
    blynk.add_read_pin_handler('V22', set_led2_handler)
    blynk.add_set_pin_handler('V23', read_rotary1_handler)
    blynk.add_set_pin_handler('V24', read_rotary2_handler)
    blynk.add_set_pin_handler('V25', read_light_handler)
    blynk.add_read_pin_handler('V26', set_slider_to_lcd_handler)

    blynk.add_handler(set_acc_handler)
    blynk.add_handler(set_rgb_led_handler)

    print("running")
    blynk.run(0.5)
    while True:
        print("sleeping")
        time.sleep(60)
