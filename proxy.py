import socket
import thread
import sys
import os
backlog = 50
MAX_DATA_ERCV =81920

def main():
    host = ''
    port = 8081
    try:
        proxy = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        proxy.bind((host, port))
        proxy.listen(backlog)
    except socket.error , (value,message):
        if proxy:
            proxy.close()
        print "Could not open socket:",message
        sys.exit(1)
    while 1:
        #create a BP socket
        conn, addr = proxy.accept()
        thread.start_new_thread(BPS,(conn,addr))
    proxy.close()

def BPS(conn,addr):
    request = conn.recv(MAX_DATA_ERCV)
    webserver = getaddr_port(request)[0]
    port = getaddr_port(request)[1]
    print webserver,port
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((webserver,port))
        s.send(request)

        while 1:
            data = s.recv(MAX_DATA_ERCV)

            if (len(data) > 0):
                conn.send(data)
            else:
                break
        s.close()
        conn.close()
    except socket.error, (value,message):
        if s:
            s.close()
        if conn:
            conn.close()
        print ('peer reset')
        sys.exit(1)

def getaddr_port(request):
    firstline = request.split('\n')[0]

    url = firstline.split(' ')[1]

    http_pos = url.find('://')

    if (http_pos==-1):
        temp = url
    else:
        temp = url[(http_pos+3):]

    port_pos = temp.find(':')

    host_pos = temp.find('/')
    if host_pos == -1:
        length = len(temp)
    
    if port_pos == -1 or length < port_pos:
        webserver = temp
        port = 80
    else:
        port = int(temp[(port_pos+1):])
        webserver = temp[:(port_pos)]
    return [webserver,port]
    


if __name__ == '__main__':
    main()

