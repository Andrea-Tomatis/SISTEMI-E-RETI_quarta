'''
Simple chat in python using TCP socket and multithreading
'''
import socket as sck
import threading as thr
import time

LOCAL = ('localhost', 5001)

class MyStringProtocol():
    def __init__(self, *args):
        self.outputString = '¬'.join(str(i) for i in args)

    def encode_msg(self):
        return self.outputString.encode()


class Connection(thr.Thread):
    def __init__(self, port, s):
        thr.Thread.__init__(self)
        self.port = port
        self.s = s
        self.running = True
    def run(self):
        while self.running:
            data, addr = self.s.recvfrom(self.port)
            msg_received = data.decode().split('¬')
            print(f"\nmessaggio arrivato da {msg_received[0]} : {msg_received[-1]}")

def main():
    #s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
    s.connect(LOCAL)
    conn = Connection(LOCAL[1], s)
    conn.start()

    s.sendall(input('tell me your nickname: ').encode())

    while True:
        time.sleep(0.2)
        receiver = input('tell me the receiver nick: ')
        if receiver.startswith('exit'):
            body = 'exit'
        else: body = input('insert a message: ')
        msg = MyStringProtocol(receiver,body)

        if body.startswith('exit'):
            msg = MyStringProtocol('None',body)
            
        s.sendall(msg.encode_msg())
        if body.startswith('exit'):
            conn.running = False
            s.close()
            conn.join()
            print('Thread killed succesfully')
            exit()
    

if __name__ == '__main__':
    main()
