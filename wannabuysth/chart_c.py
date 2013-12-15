# -*- coding: UTF-8 -*-
import socket  
import time
import gevent


def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.connect(('127.0.0.1', 8080))  
    me_id = 0
    while True:
        if not me_id:
            sock.send('me_id')  
            me_id = sock.recv(1024)
            print 'me_id ',me_id
        else:
            print sock.recv(1024)
        gevent.sleep(1)
        
    sock.close() 
    print  111
    


if __name__ == '__main__':  
    all_list = []
    for i in xrange(1000):
        all_list.append(gevent.spawn(client))
    gevent.joinall(all_list)
     

