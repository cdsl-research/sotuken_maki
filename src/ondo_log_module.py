# import upip
# upip.install("urequests")
import urequests
import ujson
from machine import I2C, Pin, RTC
import utime
import ntptime

import gc
gc.enable()

rtc = RTC()
ntptime.settime() # setup time by remote NTP server
def get_jst():
    tm = utime.localtime(utime.time()) # UTC now
    jst = str(tm[0]) + '/' + str(tm[1]) + '/' + str(tm[2]) + ' ' + str((tm[3]+9)%24) + ':' + str(tm[4]) + ':' + str(tm[5])
    return jst

def SencerAd(pinnum1, pinnum2):
    p21 = Pin(pinnum1,Pin.IN,Pin.PULL_UP)
    p22 = Pin(pinnum2,Pin.IN,Pin.PULL_UP)
    i2c =I2C(scl=Pin(pinnum2), sda=Pin(pinnum1))
    ad = 0
    if i2c.scan():
        ad = i2c.scan()
        return ad
    else:
        ad = '[No sensor.]'
        return ad

def readU5(pinnum1, pinnum2):
    p21 = Pin(pinnum1,Pin.IN,Pin.PULL_UP)
    p22 = Pin(pinnum2,Pin.IN,Pin.PULL_UP)
    i2c =I2C(scl=Pin(pinnum2), sda=Pin(pinnum1))
    readtemp = i2c.readfrom_mem(0x48,0,1)
    readtemp = int.from_bytes(readtemp,'little') & 0xFF
    return readtemp

def raw_temp(pinnum1, pinnum2):
    p21 = Pin(pinnum1,Pin.IN,Pin.PULL_UP)
    p22 = Pin(pinnum2,Pin.IN,Pin.PULL_UP)
    i2c =I2C(scl=Pin(pinnum2), sda=Pin(pinnum1))
    readtemp = readU5(pinnum1, pinnum2)
    T = ( readtemp << 8 | readU5() )>> 4
    return T

def send_server(url, header, data):
    try:
        res = urequests.post(
            url,
            data = ujson.dumps(data).encode("utf-8"),
            headers = header
        )
        print(res.status_code)
    except Exception as e:
        print(e.args)
        with open("error.log", mode='a') as f:
            f.write(get_jst() + "," + str(e.args) + "\n")
    res.close()

def event_log(date, message):
    event_data={
    "message": str(date) + ',' + str(message)
    }
    return event_data
