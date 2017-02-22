from __future__ import with_statement
import traffic_services
import time
import os
import urllib

instance = traffic_services.fetcher()
if not os.path.exists("store"):
    os.makedirs("store")

def filecmp(file1, file2):
    with open(file1) as f1:
        with open(file2) as f2:
            if f1.read() == f2.read():
                print("Duplicate file. Camera feed hasn't updated. Ignoring")
                return -1
            return 0

def start(timer, url):
    timer_min = timer * 60
    count = 0
    start_time = time.time()
    print("====\nStarting image grab at {0}\n====\n".format(time.ctime(int(time.time()))))
    minFlag = False
    hrFlag = False
    text = "sec"
    current = ""
    fileName = ""
    testfile = urllib.URLopener()

    while True:

        current = fileName
        delta = time.time() - start_time

        if delta >= 60.0:
            minFlag = True
        elif delta >= 3600 :
            hrFlag = True
        if minFlag:
            delta = delta / 60
            text = "min"
        elif hrFlag:
            delta = delta / 3600
            text = "hr"

        print("Grabbed image {:d} at delta {:f}{:s} ".format(count, delta, text))

        fileName = "image_" + str(count) + ".jpg"
        testfile.retrieve(url, "store/{:s}".format(fileName))
        count += 1
        if current is not "":
            if filecmp("store/"+fileName, "store/"+current) is -1:
                os.remove("store/"+fileName)

        time.sleep(timer_min)

URL = instance.callImage("WC", 1)
start(5, URL)