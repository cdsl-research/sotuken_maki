from utime import sleep

import gc

gc.disable()

x=0





while True:






    execfile("memori_sokutei.py")
    x=x+1
    
    if gc.mem_alloc()>gc.mem_free():
      
      gc.collect()




    sleep(10)