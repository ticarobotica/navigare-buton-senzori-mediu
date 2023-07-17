from machine import Pin, SoftI2C
from time import sleep
import bmp180, BME280
import _thread, utime
import ssd1306

i2c_bmp180=SoftI2C(sda=Pin(12), scl=Pin(13), freq=100000)
handle_bmp180=bmp180.BMP180(i2c_bmp180)

i2c_bme280=SoftI2C(sda=Pin(10), scl=Pin(11), freq=100000)
handle_bme280=BME280.BME280(i2c=i2c_bme280)

i2c_oled=SoftI2C(sda=Pin(16), scl=Pin(17), freq=100000)
oled=ssd1306.SSD1306_I2C(128, 64, i2c_oled)

buton=Pin(18, Pin.IN, Pin.PULL_UP)

global buton_apasat, nr_ecran
buton_apasat=False
nr_ecran=0

def thread_buton():
    while True:
        if buton.value()==0:
            global buton_apasat
            buton_apasat=True
        utime.sleep(0.5)
        
_thread.start_new_thread(thread_buton, ())

def get_parametrii(handle, ecran):
    if ecran==1:
        temp=handle.temperature
        press=handle.pressure
        humi=handle.humidity
        return temp, press, humi
    if ecran==2:
        temp=handle.temperature
        press=handle.pressure
        altit=handle.altitude
        return temp, press, altit
    

while True:
    global buton_apasat
    if nr_ecran==0:
        oled.text("   Senzori OFF",5,20)
    if buton_apasat==True:
        oled.fill(0)
        buton_apasat=False
        nr_ecran+=1
        if nr_ecran>2:
            nr_ecran=0
        if nr_ecran==1:
            oled.text("Senzor BME280",1,1)
            t,p,h=get_parametrii(handle_bme280, 1)
            oled.text("Temp = "+str(t),1,10)
            oled.text("Press = "+str(p),1,20)
            oled.text("Humi = "+str(h),1,30)
            
        elif nr_ecran==2:
            oled.text("Senzor BMP180",1,1)
            t,p,a=get_parametrii(handle_bmp180, 2)
            oled.text("Temp = "+str(t),1,10)
            oled.text("Press = "+str(p),1,20)
            oled.text("Alt = "+str(a),1,30)
            
        else:
            oled.text("   Senzori OFF",5,20)
        print("Nr ecran = "+str(nr_ecran), end="\r")         
    oled.show()
    utime.sleep(0.5)
    