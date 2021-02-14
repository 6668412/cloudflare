import time 
import ipaddress
import requests
import threading
import sys
import os

# fast scan spider: spider will stop scanning this ip if an cloudflare port found
def spider_fast(ip,port):
    url = ''.join(['http://',ip.strip(),':',str(port)])
    headers = {'Connection':'close'}
    try:
        r = requests.get(url,timeout=2,headers=headers)
        if r.status_code == 400:
            if 'cloudflare' in r.text:
                print (ip)
                try:
                    ip_write.append(ip)
                    ip_block_final.remove(ip)
                except:
                    pass
                control.release()
            else:
                control.release()
        else:
            control.release()
    except:
        control.release()
        pass

# fast scan main funciton
def spider_fast_main(start_port,end_port):
    print ('Executing fast scan...')
    for port in range(start_port,end_port+1):
        for ip in ip_block_final:
            control.acquire()
            t = threading.Thread(target=spider_fast,args=(ip,port,))
            t.start()
    time.sleep(10)
    with open('result.txt','a') as f:
        for i in ip_write:
            f.write(i.strip()+'\n')
    f.close()



# conprehansive spider: spider will scan all ports in order to find all cloudflare ports
def spider_conprehansive(ip,port):
    url = ''.join(['http://',ip.strip(),':',str(port)])
    headers = {'Connection':'close'}
    try:
        r = requests.get(url,timeout=2,headers=headers)
        if r.status_code == 400:
            if 'cloudflare' in r.text:
                print (url+'\t'+'Success!')
                try:
                    ip_write.append(url)
                except:
                    pass
                control.release()
            else:
                control.release()
        else:
            control.release()
    except:
        control.release()
        pass

# conprehansive scan main funciton
def spider_conprehansive_main(start_port,end_port):
    print ('Executing conprehansive scan...')
    for ip in ip_block_final:
        for port in range(start_port,end_port):
            control.acquire()
            t = threading.Thread(target=spider_conprehansive,args=(ip,port,))
            t.start()
    time.sleep(10)
    with open('result.txt','a') as f:
        for i in ip_write:
            f.write(i.strip()+'\n')
    f.close()

# test if ip is online
def pingfun(ip):
    test_online = os.popen('ping -c 2 -W 1 %s' % (ip)).read()
    if 'ttl' in test_online:
        ip_block_final.append(ip)
        control.release()
    else:
        control.release()
        pass

if __name__ == '__main__':
    start_time = time.time()
    start_port = 10000
    end_port = 65535
    ip_block_final = []
    ip_write = []
    print ('Select your choice:')
    print ('1. Enter an ip cidr.')
    print ('2. Extract from a file.')
    print ('3. Exit.')
    choice = int(input())
    if choice == 3:
        print ('Choice wrong, exit...')
        sys.exit(0)
    print ('Select a mode:')
    print ('1. Fast scan.')
    print ('2. Conprehansive scan.')
    mode = int(input())
    if choice == 1:
        ip_block_temp = ipaddress.ip_network(input('Please input an ip block:'))
        num = int(input('Please input the number of threadings:'))
        control = threading.Semaphore(num)
        ip_block = [str(iip) for iip in ip_block_temp]
        del ip_block_temp
        for ip_test in ip_block:
            control.acquire()
            t = threading.Thread(target=pingfun,args=(ip_test,))
            t.start()
        time.sleep(10)
        print ('Ip generate done')
        del ip_block
        print ('Alive ip number:'+str(len(ip_block_final)))
        if mode == 1:
            spider_fast_main(start_port,end_port)
        elif mode == 2:
            spider_conprehansive_main(start_port,end_port)
        else:
            print ('Mode wrong, exit...')
            sys.exit(0)
    elif choice == 2:
        num = int(input('Please input the number of threadings:'))
        control = threading.Semaphore(num)
        file = input('Please enter file path:')
        with open(file,'r') as f2:
            for iiip in f2:
                ip_block_final.append(iiip)
        f2.close()
        if mode == 1:
            spider_fast_main(start_port,end_port)
        elif mode == 2:
            spider_conprehansive_main(start_port,end_port)
        else:
            print ('Mode wrong, exit...')
            sys.exit(0)
    else:
        print ('Choice wrong, exit...')
        sys.exit(0)
    end_time = time.time()
    print (str(end_time-start_time))

