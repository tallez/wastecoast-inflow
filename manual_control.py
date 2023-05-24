import socket
from pynput import keyboard


Host = '192.168.1.17'
Port = 234
Socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
Socket.connect((Host,Port))


def on_press(key):
    hello = str(key.char)
    if hello == 'z':
        Command = ([0,1,0])
    elif hello == 'q':
        Command =([1,1,0])
    elif hello == 'd':
        Command =([0,1,1])

    Command = str(Command)
    Command = Command.encode('utf-8')
    Socket.send(Command)

def on_release(key):
    Command = [0,0,0]
    
    Command = str(Command)
    Command = Command.encode('utf-8')
    Socket.send(Command)

with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()