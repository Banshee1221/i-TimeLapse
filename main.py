import traffic_services
import time
import os.path
import urllib


instance = traffic_services.fetcher()
if not os.path.exists("store"):
    os.makedirs("store")

def start(timer, url):
    timer_min = timer * 60
    count = 0
    start_time = time.time()
    print "====\nStarting image grab at {0}\n====\n".format(time.ctime(int(time.time())))
    while True:
        print "Grabbed image {:d} at delta {:f}s ".format(count, (time.time() - start_time))
        testfile = urllib.URLopener()
        testfile.retrieve(url, "store/image_"+str(count)+".jpg")
        count += 1
        time.sleep(timer_min)

URL = instance.callImage("WC", 1)
start(5, URL)