import requests
import re
import threading
import time
import sys
import os



# spider function
# I decided to put circulation outside the function
# this function return result ip address
def spider(url,port):
    url = 'http://'+str(url)+':'+str(port)
    try:
        r = requests.get(url,timeout=2)
        if r.status_code == 400:
            if 'cloudflare' in r.text:
                print (url.strip()+'\t'+'success\n')
                control.release()
            else:
                control.release()
                pass
        else:
            control.release()
            pass
    except:
        control.release()
        pass


# create threadings
if __name__ == "__main__":
    start_time = time.time()
    start_port = 10000
    end_port = 65535
    num = 100
    with open('to_scan.txt','r') as f:
        ipverified = [ip for ip in f]
    f.close()
    control = threading.Semaphore(num)
    for ip_pass in ipverified:
        ip_pass = ip_pass.strip()
        print (ip_pass+'\n')
        for ports in range(start_port,end_port+1):
            control.acquire()
            t = threading.Thread(target=spider,args=(ip_pass,ports,))
            t.start()
    time.sleep(2)
    end_time = time.time()
    print (str(end_time - start_time))
