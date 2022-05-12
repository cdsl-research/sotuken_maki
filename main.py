import utime
import ondo_log_module
import sys
from machine import I2C, Pin, RTC

# tm = utime.localtime(utime.time())
# minite_jst = int(tm[4])
# while minite_jst % 5 != 0:
#     print(str(minite_jst))
#     tm = utime.localtime(utime.time())
#     minite_jst = int(tm[4])
#     utime.sleep(1) 
    


# execfile("repetition.py")

# 1days = 300 * 12 * 24
for i in range(12*24):
    # tm_b = utime.localtime(utime.time()) # UTC now
    # print(tm_b)
    impl=sys.implementation
    lang_version = str(impl[0])+","+str(impl[1])

    plat=sys.platform

    print(ondo_log_module.get_jst())

    log = ondo_log_module.get_jst()+","+str(ondo_log_module.SencerAd(21, 22))+","+lang_version+","+plat
    print(log)

    with open("ab.log", mode='a') as f:
        f.write(log + "\n")

    url = 'http://ono-http-setver.a910.tak-cslab.org:8888'
    header = {
                'Content-Type' : 'application/json'
    }

    ondo_log_module.send_server(url + '/event_log', header, ondo_log_module.event_log(ondo_log_module.get_jst(), "ログを生成しました"))


    log_data={
        "message":log
    }

    ondo_log_module.send_server(url + '/post_data', header, log_data)
    ondo_log_module.send_server(url + '/event_log', header, ondo_log_module.event_log(ondo_log_module.get_jst(), "ログを送信しました"))


    temp = ondo_log_module.raw_temp(21, 22) * 0.0625
    print(temp)
    temp_data = {
        "message":str(temp)
    }
    ondo_log_module.send_server(url + '/event_log', header, ondo_log_module.event_log(ondo_log_module.get_jst(), "温度データを取得しました"))

    ondo_log_module.send_server(url + '/send_temp', header, temp_data)
    ondo_log_module.send_server(url + '/event_log', header, ondo_log_module.event_log(ondo_log_module.get_jst(), "温度データを送信しました"))


    # execfile("ondo_log.py")

    # tm_a = utime.localtime(utime.time()) # UTC now
    # print(tm_a)

    # print(utime.ticks_diff(tm_a - tm_b))

    # utime.sleep(10 - utime.ticks_diff(tm_a - tm_b))

    utime.sleep(300)

# execfile("main.py")
