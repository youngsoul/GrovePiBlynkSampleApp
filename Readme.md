GrovePi / Blynk Sample applications
===================================


The purpose of this sample application was to test the integration of grovepi, blynk and the PyBlynkRestApi module.

GrovePI was setup on a Raspberry PI with the following Sensors:

Button: GrovePI D6 - Blynk V20

LED: GrovePI D3 - Blynk V21

LED: GrovePI D5 - Blynk V22

RGB LED: GrovePI D2 - Blynk (r)V30,(g)V31,(b)V32

3 Axis Accelerometer: GrovePI I2C - Blynk (x)V27, (y)V28, (z)V29

Rotary: GrovePI A0 = Blynk V23

Rotary: GrovePI A1 - Blynk V24

Light Sensor: GrovePI A2 - Blynk V25

RGB LCD: GrovePI I2C - Blynk V26

To Execute on Raspberry PI
--------------------------

This implementation assumes Python 3.x and has not been tested yet with Python 2.7.x.

python3 main.py

The main.py file assumes there is a file called 'auth_token.txt' which has a single line with the Blynk Authortization Token.

Blynk Application 
-----------------

![Alt text](./images/IMG_4504.PNG "Tab 1")
![Alt text](./images/IMG_4505.PNG "Tab 1")

PyBlynkRestApi Project
----------------------

https://github.com/youngsoul/PyBlynkRestApi

A picture of the Raspberry PI with the GrovePI sensors is below:

![Alt text](./images/IMG_4509.JPG "Tab 1")
