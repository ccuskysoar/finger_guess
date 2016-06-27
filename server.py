import socket
import threading
import time
import string

MAX_BYTES = 65535
mylist = list()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1',1061))
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.listen(5)
print('Listening at', sock.getsockname())
def server():
    while True:
         connection, addr = sock.accept()
         print('Accept a new connection', connection.getsockname(), connection.fileno())
         try:
            mythread = threading.Thread(target=subThreadIn, args=(connection, connection.fileno()))
            mythread.setDaemon(True)
            mythread.start()
         except :
            pass

def tellOthers(exceptNum, whatToSay):
    for c in mylist:
        if c.fileno() != exceptNum :
            try:
                c.send(whatToSay.encode())
            except:
                pass

def subThreadIn(myconnection, connNumber):
    flag = -1
    mylist.append(myconnection)
    while True:
        try:
            recvedMsg = myconnection.recv(MAX_BYTES).decode()
            if recvedMsg:
               print(recvedMsg)
               tellOthers(connNumber,recvedMsg)
        except (OSError, ConnectionResetError):
            try:
                mylist.remove(myconnection)
            except:
                pass
            myconnection.close()
            return

if __name__ == '__main__':
        server()
