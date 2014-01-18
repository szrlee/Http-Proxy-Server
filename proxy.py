import socket
import threading
import sys
backlog = 50
MAX_DATA_ERCV =999999

def main():
    host = ''
    port = 8087
    try:
        proxy = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        proxy.bind((host,port))
        proxy.listen(backlog)
    except socket.error , (value,message):
        if proxy:
            proxy.close()
        print "Could not open socket:",message
        sys.exit(1)
#receive request from browser B_P_S loop to end
#send data to proxy S_P_B loop to end
#use threading
#still needing code
