import urequests
import ujson
from machine import I2C, Pin, RTC
import utime
import ntptime
import sys

p21 = Pin(21,Pin.IN,Pin.PULL_UP)
p22 = Pin(22,Pin.IN,Pin.PULL_UP)
i2c =I2C(scl=Pin(22), sda=Pin(21))

rtc = RTC()
ntptime.settime() 

tm = utime.localtime(utime.time()) # UTC now

datetime_jst = str(tm[0])+'/'+str(tm[1])+'/'+str(tm[2])+' '+str((tm[3]+9)%24)+':'+str(tm[4])+':'+str(tm[5])


def readU5():

    readtemp = i2c.readfrom_mem(0x48,0,1)
    readtemp = int.from_bytes(readtemp,'little') & 0xFF
    return readtemp

def raw_temp():

    readtemp = readU5()
    T = ( readtemp << 8 | readU5() )>> 4
    return T

#temp = raw_temp() * 0.0625

def SencerAd():

    ad = 0

    if i2c.scan():

        ad = i2c.scan()

        return ad

    else:

        ad = '[No sensor.]'

        return ad

#print(datetime_jst)
#print(i2c)
#print(SencerAd())
#print(sys.implementation)
#print(sys.platform)

#print(temp)

impl=sys.implementation

lang_version = str(impl[0])+","+str(impl[1])

plat=sys.platform

log = datetime_jst+","+str(SencerAd())+","+lang_version+","+plat
print(log)

with open("ab.log", mode='a') as f:
  f.write(log + "\n")
 

#url = 'http://192.168.100.63/maki_test_http_request.php'
url = 'http://192.168.100.31:8888/post_data'

data={
    "message":log
}



header = {
            'Content-Type' : 'application/json'
        }

res = urequests.post(
        url,
        data = ujson.dumps(data).encode("utf-8"),
        headers = header
    )

print(res.status_code)

res.close()