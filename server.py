import socket
import threading
import time
import string

MAX_BYTES = 65535
mylist = list()

mydict = dict()
gamedict = dict()
gamelist = list()  # just record players

nameToscore = dict()  # record the play's score


getPoint = 0
gamePoint = [0,0]
gamePicture = ['0','    ','0','    ','0','    ','0','\n',
               '0','    ','0','    ','0','    ','0','\n',
               '0','    ','0','    ','0','    ','0','\n',
               '0','    ','0','    ','0','    ','0','\n']

gameToString = ''

for i in gamePicture:
    gameToString = gameToString + i





GameCount = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1',9521))
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
                content = mydict[exceptNum] + ' say: '+ whatToSay
                c.send(content.encode())
            except:
                pass

def tellAll(exceptNum, whatToSay):
    for c in mylist:
        try:    
            c.send(whatToSay.encode())
            time.sleep(1)
        except:
            pass
    


def game(A, whoA, B, whoB):
    global getPoint
    if A == 'Cut' and B == 'Par' or A == 'Sto' and B == 'Cut' or A == 'Par' and B == 'Sto':
        if A == 'Cut':
            print("****")
            print(nameToscore[whoA]*2)
            gamePicture[ nameToscore[whoA]*2 ] = '0' # let old position = 0 
            getPoint = 2
            nameToscore[whoA] +=2
           # gamePoint[0] += 2
            if nameToscore[whoA] <= 15: # still not Fin
                gamePicture[ nameToscore[whoA]*2 ] = whoA[0]
            else:  # after add this one will Fin 
                gamePicture[30] = whoA[0]


        elif A == 'Sto':
            print("****")
            print(nameToscore[whoA]*2)
            gamePicture[ nameToscore[whoA]*2 ] = '0'
            getPoint = 1
            nameToscore[whoA] +=1
           # gamePoint[0] += 1
            if nameToscore[whoA] <= 15: # still not Fin          
                gamePicture[ nameToscore[whoA]*2 ] = whoA[0]
            else:
                gamePicture[30] = whoA[0]

        else:
            gamePicture[ nameToscore[whoA]*2 ] = '0'
            getPoint = 5
            nameToscore[whoA] +=5
           # gamePoint[0] += 5
            if nameToscore[whoA] <= 15: # still not Fin  
                gamePicture[ nameToscore[whoA]*2 ] = whoA[0]
            else:
                gamePicture[30] = whoA[0]

        
        # if someone be chase, the one must to back 1 step 
        if nameToscore[whoA] == nameToscore[whoB]:
            nameToscore[whoB] -= 1
            gamePicture[ nameToscore[whoB]*2 ] = whoB[0]

        return whoA

    elif A == 'Cut' and B == 'Sto' or A == 'Sto' and B == 'Par' or A == 'Par' and B == 'Cut':
        if A == 'Cut':
            gamePicture[ nameToscore[whoB]*2 ] = '0' # let old position = 0
            getPoint = 1
            nameToscore[whoB] +=1 
           # gamePoint[1] += 1
            if nameToscore[whoB] <= 15:
                gamePicture[ nameToscore[whoB]*2 ] = whoB[0]
            else:
                gamePicture[30] = whoB[0]
    
        elif A == 'Sto':
            gamePicture[ nameToscore[whoB]*2 ] = '0'
            getPoint = 5
            nameToscore[whoB] +=5
           # gamePoint[1] += 5
            if nameToscore[whoB] <= 15:
                gamePicture[ nameToscore[whoB]*2 ] = whoB[0]
            else:
                gamePicture[30] = whoB[0]  

        else:
            gamePicture[ nameToscore[whoB]*2 ] = '0'        
            getPoint = 2
            nameToscore[whoB] +=2
           # gamePoint[1] += 2
            if nameToscore[whoB] <= 15:
                gamePicture[ nameToscore[whoB]*2 ] = whoB[0]
            else:
                 gamePicture[30] = whoB[0]  
         # if someone be chase, the one must to back 1 step 
        if nameToscore[whoB] == nameToscore[whoA]:
            nameToscore[whoA] -= 1
            gamePicture[ nameToscore[whoA]*2 ] = whoA[0]


        return whoB
    
    else:
        return 2 
def subThreadIn(myconnection, connNumber):

    name = myconnection.recv(1024).decode()
    # print(name)
    mydict[myconnection.fileno()] = name # maybe not
    
    nameToscore[name] = 0  ######### score
    global Gamecount
    global gameToString    

    flag = -1
    mylist.append(myconnection) #
    while True:
        try:
            recvedMsg = myconnection.recv(MAX_BYTES).decode()
            
            if recvedMsg:
                if recvedMsg[0] == '@':
                    gamedict[name] = recvedMsg[1:] #otis use  
                   # gamelist[GameCount] = name # array 0 is otis
                    gamelist.append(name)
                                      
                   # GameCount += 1

                   # gamelist[GameCount] = 'john'# array 1 is john
                 #   gamelist.append('john')
                    print(gamelist)
                #    gamedict['john'] = 'Cut'# john use 
                    
                    if len(gamedict) == 2:
                       result = game(gamedict[gamelist[0]], gamelist[0], gamedict[gamelist[1]], gamelist[1])
                      
                    
                       gameToString = '' # reset string
                       for i in gamePicture:
                           gameToString = gameToString + i
                       
                      # for i in range(0, len(gamePicture), +1): # reset source picture
                      #     if gamePicture[i]  != '0' or gamePicture[i] != ' '  :
                      #          gamePicture[i] = '0' 

                       if result != 2:
                          # print(result)
                          # print(gamelist[result])
                                                      
                           for i in range(0, len(gamelist), +1):
                               if gamelist[i] == result:
                                   tellAll(connNumber, '@'+ gamelist[i])
                                   time.sleep(0.25) 
                                   tellAll(connNumber, '#'+ gameToString)
                                  # time.sleep(2)  
                                  # time.sleep(1)

                           # game is over 
                           if nameToscore[result] >= 15:
                               # all the score is back to zero
                               for i in range(0, len(gamelist), +1):
                                   nameToscore[ gamelist[i] ] = 0
                                      

                               for i in range(0, len(gamePicture), +1): # reset source picture
                                   if gamePicture[i] != '0' and gamePicture[i] != '    ' and gamePicture[i] != '\n' :
                                       gamePicture[i] = '0'                                

                               
                               for i in gamePicture:
                                   print(i, end="")

                               tellAll(connNumber, '#'+ '@'+ result + ' Win the game!!' )

                                     

                       else:
                           tellAll(connNumber, '@same')
                           time.sleep(1)
                           tellAll(connNumber, '#'+ gameToString)
                               
                       gamelist.pop(0)
                       gamelist.pop(0)    
                       gamedict.popitem()
                       gamedict.popitem()                         
                    #   GameCount = 0
                          
                
                else:
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

