from tkinter import *
import socket
import threading
from getpass import getpass
import time
import string

MAX_BYTES = 65535
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1',1061))

def sendpaper():
    content = 'xxxpaperxxx'
    game_output.insert(END,content)

def sendscissors():
    content = 'xxxscissorsxxx'
    game_output.insert(END,content)

def sendstone():
    content = 'xxxstonexxx'
    game_output.insert(END,content)

def sendmsg():
    msgcontent = 'I say: '
    talk_output.insert(END, msgcontent)
    talk_output.insert(END, talk_input.get('0.0', END))
    sock.send(talk_input.get('0.0', END).encode())
    talk_input.delete('0.0', END)

def client():
    th2 = threading.Thread(target=recvThreadFunc)
    th2.setDaemon(True)
    th2.start()

def recvThreadFunc():
    while True:
        try:
            otherword = sock.recv(MAX_BYTES)
            if otherword:
                print(otherword.decode())
                msg = 'Others say: '+ otherword.decode()
                talk_output.insert(END,msg)
            else :
                pass
        except ConnectionResetError:
            print('Server is closed!')

client()

#GUI
root = Tk()
root.title("Finger-Guessing Game")
#creat frame for container        
frame_left_top   = Frame(width=500, height=400)
frame_left_paper = Frame(width=166, height=30)
frame_left_scissors = Frame(width=166, height=30)
frame_left_stone = Frame(width=168, height=30)
frame_right_top   = Frame(width=300, height=360, bg='white')
frame_right_center  = Frame(width=300, height=40, bg='white')
frame_right_btn  = Frame(width=300, height=30)
#use grid to set frame 
frame_left_top.grid(row=0, column=0, columnspan=3,rowspan=3, padx=4, pady=5)
frame_left_paper.grid(row=2, column=0)
frame_left_scissors.grid(row=2, column=1)
frame_left_stone.grid(row=2, column=2)
frame_right_top.grid(row=0, column=3)
frame_right_center.grid(row=1, column=3)
frame_right_btn.grid(row=2, column=3)
#lock frame by container
frame_left_top.grid_propagate(0)
frame_left_paper.grid_propagate(0)
frame_left_scissors.grid_propagate(0)
frame_left_stone.grid_propagate(0)
frame_right_top.grid_propagate(0)
frame_right_center.grid_propagate(0)
frame_right_btn.grid_propagate(0)
#create object(text button)
game_output = Text(frame_left_top)
game_paper = Button(frame_left_paper, text='paper', command=sendpaper)
game_scissors = Button(frame_left_scissors, text='scissors', command=sendscissors)
game_stone = Button(frame_left_stone, text='stone', command=sendstone)
talk_output = Text(frame_right_top)
talk_input = Text(frame_right_center)
talk_send = Button(frame_right_btn, text='send', command=sendmsg )
#input object to frame
game_output.grid()
game_paper.grid()
game_scissors.grid()
game_stone.grid()
talk_output.grid()
talk_input.grid()
talk_send.grid()

root.mainloop()
