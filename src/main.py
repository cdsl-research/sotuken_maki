import utime
import new_module
import sys
from machine import I2C, Pin, RTC
import gc

# tm = utime.localtime(utime.time())
# minite_jst = int(tm[4])
# while minite_jst % 5 != 0:
#     print(str(minite_jst))
#     tm = utime.localtime(utime.time())
#     minite_jst = int(tm[4])
#     utime.sleep(1) 
    

#ガベージ
gc.enable
mem = gc.mem_alloc()+gc.mem_free()

# execfile("repetition.py")

# 1days = 300 * 12 * 24
for i in range(12*24*5):
    # tm_b = utime.localtime(utime.time()) # UTC now
    # print(tm_b)
    impl=sys.implementation
    lang_version = str(impl[0])+","+str(impl[1])

    plat=sys.platform

    print(new_module.get_jst())

    mem_pa = int(gc.mem_alloc()/mem*100)

    log = new_module.get_jst()+","+str(new_module.SencerAd(21, 22))+","+lang_version+","+plat+", memory usage"+ str (mem_pa)+"%"
    print(log)

    with open("ab.log", mode='a') as f:
        f.write(log + "\n")

    url = 'http://ono-http-setver.a910.tak-cslab.org:8888'
    header = {
                'Content-Type' : 'application/json'
    }

    new_module.send_server(url + '/event_log', header, new_module.event_log(new_module.get_jst(), "ログを生成しました"))


    log_data={
        "message":log
    }

    new_module.send_server(url + '/post_data', header, log_data)
    new_module.send_server(url + '/event_log', header, new_module.event_log(new_module.get_jst(), "ログを送信しました"))


    temp = new_module.raw_temp(21, 22) * 0.0625
    print(temp)
    temp_data = {
        "message":str(temp)
    }
    new_module.send_server(url + '/event_log', header, new_module.event_log(new_module.get_jst(), "温度データを取得しました"))

    new_module.send_server(url + '/send_temp', header, temp_data)
    new_module.send_server(url + '/event_log', header, new_module.event_log(new_module.get_jst(), "温度データを送信しました"))


    # execfile("ondo_log.py")

    # tm_a = utime.localtime(utime.time()) # UTC now
    # print(tm_a)

    # print(utime.ticks_diff(tm_a - tm_b))

    # utime.sleep(10 - utime.ticks_diff(tm_a - tm_b))

    gc.collect()
    utime.sleep(300)

# execfile("main.py")

