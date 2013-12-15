# -*- coding: UTF-8 -*-
import os
if os.name!='nt':
    from twisted.internet import epollreactor
try:
    epollreactor.install()
except:
    pass
else:
    from twisted.internet import iocpreactor as iocpreactor
try:
    iocpreactor.install()
except:
    pass
import sys
from twisted.internet import protocol, reactor
from twisted.internet import protocol
from twisted.protocols import basic
from twisted.python import log
from twisted.internet import reactor


class ConfigServer(basic.LineReceiver):
    def __init__(self):
        pass
    
    def lineReceived(self, line):
        if line == 'quit':
            self.sendLine('Goodbye.')
            self.transport.loseConnection()
        else:
            self.broadcast(line)
    
    def broadcast(self, msg):
        for client in self.factory.clients:
            client.sendLine(' % s said: % s' % (self.transport.getPeer().host, msg));
            
    def connectionMade(self):
        self.factory.clients.append(self)
        print 'Connect from % s..' % self.transport.getHost()
        self.sendLine('Welcome… % s' % self.transport.getHost())
        
    def connectionLost(self, reason):
        self.factory.clients.remove(self)

class ConfigServerFactory(protocol.ServerFactory):
    protocol = ConfigServer
    clients = []

def main():
    log.startLogging(sys.stdout)
    reactor.listenTCP(8080, ConfigServerFactory())
    reactor.run()
    
if __name__ == '__main__':
    main()

