# Written by S. Mevawala, modified by D. Gitzel

import logging

import channelsimulator
import utils
import sys
import socket

import hashlib

class Receiver(object):

    '''
    #ACK_DATA -> ACK response handed back to sender
    #Should return the packet number sent if it recieves correct packet
    #otherwise return last correctly recieved packet.
    #curack -> current ACK number
    
    curack = 0
    ACK_DATA = bytes(curack)
    '''

    def __init__(self, inbound_port=50005, outbound_port=50006, timeout=0.001, debug_level=logging.INFO):
        self.logger = utils.Logger(self.__class__.__name__, debug_level)

        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port,
                                                           debug_level=debug_level)
        self.simulator.rcvr_setup(timeout)
        self.simulator.sndr_setup(timeout)

    def receive(self):

        #To differentiate the handshake triggers from everything else.
        #It's unlikely that random data will contain specifically "handshake," but just in case
        
        gethand = False
        startcount = False

        #expected number of packets received
        expcount = 0

        #getting the handshake from sender
        
        while gethand == False:
            
            try:
                handshake = self.simulator.u_receive()
                checkthis = handshake[0:16] #should be checksum
                numberthis = handshake[16:24] #should be total number of packets expected
                hashthis = handshake[16:] #contains both number and data, is what checksum checked
                decodethis = handshake[24:] #should be data "handshake"
                checkingthis = hashlib.md5() 
                checkingthis.update(hashthis) 
                checkedthis = checkingthis.digest() #creating another hash
                if checkthis == checkedthis and decodethis.decode('ascii') == 'handshake':
                    gethand = True
                    expcount = int(numberthis.decode('ascii'))
                    
                    acksend = bytearray('handshake','ascii','strict')
                    ackcheck = hashlib.md5()
                    ackcheck.update(acksend)
                    acksum = ackcheck.digest()
                    acksent = acksum + acksend
                    self.simulator.u_send(acksent) #send back the handshake ack to sender
                    self.logger.info("Got data from socket: {}".format(
                        decodethis.decode('ascii')))  # note that ASCII will only decode bytes in the range 0-127
            
            except socket.timeout:
                pass

        #running the data from sender

        pktrcv = 0 #packets received thus far

        datadict = {} #dictionary of data. Key is the sequence number. Value is the data.
        #Want to call upon dictionary keys in order at the end to write to output file.
        
        while pktrcv < expcount:
            try:
                #sys.stderr.write("At receiver data loop\n")
                data = self.simulator.u_receive()
                checkdata = data[0:16] #checksum data
                numberdata = data[16:24] #sequence number data
                hashdata = data[16:]
                decodedata = data[24:]
                checkingdata = hashlib.md5()
                checkingdata.update(hashdata) 
                checkeddata = checkingdata.digest() #current hash checksum
                
                if checkdata == checkeddata:
                    dictkeyint = int(numberdata.decode('ascii'))
                    if dictkeyint == 0: #getting the first "0" packet signifies first seq packet
                        gethand = True 
                    dictkey = str(dictkeyint) #mostly for ack formatting and dictionary keys

                    isNone = datadict.get(dictkey) #checks if that key exists in dictionary
                    datadict[dictkey] = decodedata.decode('ascii') #sets key and value regardless
                    
                    if (gethand == True): #Until this is True, pktrcv won't increment
                        if isNone == None: #Also if the seq num is already recorded, no increment
                            pktrcv += 1

                        acksend = bytearray(dictkey,'ascii','strict')
                        ackcheck = hashlib.md5()
                        ackcheck.update(acksend)
                        acksum = ackcheck.digest()
                        acksent = acksum + acksend
                        self.simulator.u_send(acksent) #sends ack of packet with sequence number
                        
                    else: #this sends the handshake ack back again
                        acksend = bytearray('handshake','ascii','strict')
                        ackcheck = hashlib.md5()
                        ackcheck.update(acksend)
                        acksum = ackcheck.digest()
                        acksent = acksum + acksend
                        self.simulator.u_send(acksent)
                        
                    self.logger.info("Got data from socket: {}".format(
                        decodedata.decode('ascii')))  # note that ASCII will only decode bytes in the range 0-127
            
            except socket.timeout:
                pass


        #Whole thing this does is just print everything out in dictionary in order
        countdata = 0
        while countdata < pktrcv:
            sys.stdout.write(datadict[str(countdata)])
            countdata += 1
        
        #raise NotImplementedError("The base API class has no implementation. Please override and add your own.")


class BogoReceiver(Receiver):
    ACK_DATA = bytes(123)

    def __init__(self):
        super(BogoReceiver, self).__init__()

    def receive(self):
        self.logger.info("Receiving on port: {} and replying with ACK on port: {}".format(self.inbound_port, self.outbound_port))
        while True:
            try:
                 data = self.simulator.u_receive()  # receive data
                 self.logger.info("Got data from socket: {}".format(
                     data.decode('ascii')))  # note that ASCII will only decode bytes in the range 0-127
	         sys.stdout.write(data)
                 #print(data)
                 self.simulator.u_send(BogoReceiver.ACK_DATA)  # send ACK
            except socket.timeout:
                sys.exit()

if __name__ == "__main__":
    # test out BogoReceiver
    #rcvr = BogoReceiver()
    rcvr = Receiver()
    rcvr.receive()
