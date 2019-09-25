# Written by S. Mevawala, modified by D. Gitzel

import logging
import socket

import channelsimulator
import utils
import sys

import hashlib

def slice_frames(data_bytes):
    """
    Slice input into BUFFER_SIZE frames
    :param data_bytes: input bytes
    :return: list of frames of size BUFFER_SIZE
    """
    frames = list()
    num_bytes = len(data_bytes)
    extra = 1 if num_bytes % 1000 else 0

    for i in xrange(num_bytes / 1000 + extra):
        frames.append(
            data_bytes[
                i * 1000:
                i * 1000 + 1000
            ]
        )
    return frames

class Sender(object):

    def __init__(self, inbound_port=50006, outbound_port=50005, timeout=0.001, debug_level=logging.INFO):
        self.logger = utils.Logger(self.__class__.__name__, debug_level)

        self.inbound_port = inbound_port
        self.outbound_port = outbound_port
        self.simulator = channelsimulator.ChannelSimulator(inbound_port=inbound_port, outbound_port=outbound_port,
                                                           debug_level=debug_level)
        self.simulator.sndr_setup(timeout)
        self.simulator.rcvr_setup(timeout)

    def send(self, data):
        
        self.logger.info("Sending on port: {} and waiting for ACK on port: {}".format(self.outbound_port, self.inbound_port))

        #window -> describes the window size of SR.

        #windarr -> an array that stores the status of packets sent. Works by modulo:
        #For example, windarr[0] can represent 0, 20, 40, depending on where window is.
        #windarr[1] can represent 1, 21, 41. Etc, etc.
        #0 entry represents ACK for the packet has not been received
        #1 entry represents ACK for packet has been received
        #-1 represents there are no more packets left to send for that modulo.
        
        window = 20
        windarr = [0] * window

        #allsent -> checks if all the packets are sent in a window.
        #if there are any 0 entries in windarr, allsent should become False

        allsent = True

        '''
        Step 1: Prepare what needs to be sent:
        '''

        #rawdata -> frames of data that should be sent. This takes 1000 bytes at a time
        #slice_frames is taken from the simulation code, modified to take 1000 instead of 1024 bytes
        #The 24 byte disparity is reserved space for the checksum and the sequence number
        
        rawdata = slice_frames(data)

        #sentdata -> array of all the data that needs to be sent to the receiver 
        #seqnum -> records how many entries are in sentdata, assigns sequence numbers to packets

        sentdata = []
        seqnum = 0

        #Aim of loop:
        #1: Take each packet data
        #2: Put sequence number seqnum in front of it
        #3: Calculate the data's checksum
        #4: Put the checksum in front of the combined seqnum and packet data segment
        #5: Append this total segment into sentdata, increment seqnum
        
        for chunk in rawdata:
            seqstr = '{:<8}'.format(str(seqnum))
            seqbyte = bytearray(seqstr, 'ascii', 'strict')
            seqchunk = seqbyte + chunk
            m = hashlib.md5()
            m.update(seqchunk)
            digested = m.digest()
            testbytes = digested + seqchunk
            sentdata.append(testbytes)
            seqnum += 1

            
        '''
        Step 2: Establishing Connection With Receiver
        '''
            
        #Before running any actual data sending, need to establish handshake
        #And more importantly tell receiver how many packets it should expect

        #Once receiver confirms picking up handshake, confirmed set to True
        
        confirmed = False
        message = '{:<8}'.format(str(seqnum)) + 'handshake'
        handshake = bytearray(message,'ascii','strict')
        cheksum = hashlib.md5()
        cheksum.update(handshake)
        digested2 = cheksum.digest()
        handsent = digested2 + handshake
        
        while confirmed == False:
            try:
                self.simulator.u_send(handsent) # send data
                handack = self.simulator.u_receive()  # receive ACK
                checkthis = handack[0:16]

                decodethis = handack[16:]
                checkingthis = hashlib.md5()
                checkingthis.update(decodethis)
                checkedthis = checkingthis.digest()

                if checkthis == checkedthis and decodethis.decode('ascii') == 'handshake':

                    confirmed = True
                
            except socket.timeout:
                pass
            
            
        winstart = 0
        winnow = 0
        winend = winstart + 20

        #There is the scenario that in the last sequence
        #The receiver may send a garbled ack back, causing the sender
        #to want to continue sending
        #However, the receiver DID get all the data and therefore
        #is no longer running
        #In that case, if the program loops around at the end too many times
        #I will assume that the receiver closed because it's finished
        #and terminate this loop
        
        maxcount = 0
        
        while (winnow < seqnum or allsent == False):

            
            #Every time reach end of window or end of sentdata:
            #Check if there are any unsent packets
            #If there are, need to resend, set winstart back to window size
            #Else, set winstart to current window value, reset winend
            
            if (winnow == winend or winnow >= seqnum):
                
                #In the scenario of reaching the end of sentdata,
                #it is possible remaining data size is less than 20
                #Set nonexistent data entries to -1 so will not access unassigned data
                #and crash the program for no reason

                
                if (winnow >= seqnum):
                    notthere = (seqnum - 1) % window
                    index = 0
                    while index < window:
                        if index > notthere:
                            windarr[index] = -1
                        index += 1
                
                for rcv in windarr:
                    if rcv == 0:
                        allsent = False
                        break
                    else:
                        allsent = True

                if (allsent == False):

                    if (winnow >= seqnum - 1):
                        maxcount += 1

                    if (maxcount > 4):
                        #print("Breaking Sender Loop at maxcount")
                        break
                    else:
                        winnow = winstart

                elif(winnow >= seqnum):
                    #print("Breaking Sender Loop since it should end, allsent is true at the end")
                    break
                    
                else:
                    winstart = winnow
                    winend = winstart + 20
                    windarr = [0] * window
                    allsent = False

            
            #If not at end of window or end of sentdata:
            #Send packets if no confirmation of packet exists
            
            try:
            
                curind = winnow % window


                if (windarr[curind] == 0):

                    
                    self.simulator.u_send(sentdata[winnow]) # send data
                    ack = self.simulator.u_receive()  # receive ACK
                    checkthis2 = ack[0:16]

                    decodethis2 = ack[16:]
                    checkingthis2 = hashlib.md5()
                    checkingthis2.update(decodethis2)
                    checkedthis2 = checkingthis2.digest()

                    if checkthis2 == checkedthis2 and decodethis2.decode('ascii') == str(winnow):

                        windarr[curind] = 1  

                        self.logger.info("Got ACK from socket: {}".format(
                            decodethis2.decode('ascii')))  # note that ASCII will only decode bytes in the range 0-127
                      
                    
            except socket.timeout:
                pass

            finally:
                winnow += 1

        #raise NotImplementedError("The base API class has no implementation. Please override and add your own.")


class BogoSender(Sender):

    def __init__(self):
        super(BogoSender, self).__init__()

    def send(self, data):
        self.logger.info("Sending on port: {} and waiting for ACK on port: {}".format(self.outbound_port, self.inbound_port))
        while True:
            try:

                #want to see what sliced frames look like

                test = slice_frames(data)
                #print(test)

                checksums = []
                seqnum = 0
                for chunk in test:
                    seqstr = '{:<8}'.format(str(seqnum))
                    seqbyte = bytearray(seqstr, 'ascii', 'strict')
                    seqchunk = seqbyte + chunk
                    m = hashlib.md5()
                    m.update(seqchunk)
                    digested = m.digest()
                    testbytes = digested + seqchunk
                    checksums.append(testbytes)
                    seqnum += 1
                    #print m.digest_size

                print checksums[0]

                self.simulator.u_send(data)  # send data
                ack = self.simulator.u_receive()  # receive ACK
                self.logger.info("Got ACK from socket: {}".format(
                    ack.decode('ascii')))  # note that ASCII will only decode bytes in the range 0-127
                break
            except socket.timeout:
                pass


if __name__ == "__main__":
    # test out BogoSender
    DATA = bytearray(sys.stdin.read())
    #print DATA[1]
    #sndr = BogoSender()
    sndr = Sender()
    sndr.send(DATA)
