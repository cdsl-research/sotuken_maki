from machine import RTCimport utimeimport ntptimertc = RTC()ntptime.settime() tm = utime.localtime(utime.time()) # UTC nowjst = str(tm[0])+'/'+str(tm[1])+'/'+str(tm[2])+' '+str((tm[3]+9)%24)+':'+str(tm[4])+':'+str(tm[5])print(jst)