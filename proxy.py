import socket
import thread
import sys
import os

backlog = 50
MAX_DATA_RECV = 81920

def main():
    host = ''
    port = 8089
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(backlog)
    except socket.error, (value, message):
        if server:
            server.close()
        print "Could not open socket:", message
        sys.exit(1)

    while 1:
        conn, client_addr = server.accept()
        #create a BP socket
        thread.start_new_thread(BPS, (server, conn, client_addr))
            
    server.close()


def BPS(server, conn, client_addr):
    request = conn.recv(MAX_DATA_RECV)
    print request
    got = getaddr_port(request)
    (firstline, webserver, port) = (got[0],got[1],got[2])
    print webserver, port
    print firstline
    print client_addr 
    thread.start_new_thread(SPB,(request, conn, webserver, port))

    
def SPB(request, conn, webserver, port):
    try:
        proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy.connect((webserver, port))
        #ssl_conn = 'CONNECT %s:%s HTTP/1.1\r\n' % (webserver, port)
        #useragent = 'User-Agent: Mozilla/5.0\r\n'
        #proxy_connection = 'Proxy-Connection: Keep-alive\r\n'
        #connection = 'Connection: keep-alive\r\n'
        #Host = 'Host: %s\r\n' % webserver
        #proxy_pieces = ssl_conn+useragent+proxy_connection+connection+Host+'\r\n'
        #print proxy_pieces
        #proxy.sendall(proxy_pieces+'\r\n')
        #response = proxy.recv(MAX_DATA_RECV)
       # status = response.split(None, 1)[1]
       # if int(status)/100 !=2:
        #    print 'error', response 
         #   raise RuntimeError(status)
       # else:
        proxy.sendall(request)

        while 1:
            data = proxy.recv(MAX_DATA_RECV)

            if (len(data) > 0):
                conn.send(data)
            else:
                break
        proxy.close()
        conn.close()
    except socket.error, (value, message):
        if proxy:
            proxy.close()
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

    webserver_pos = temp.find('/')

    if webserver_pos== -1:
        webserver_pos = len(temp)
   
    webserver = ''
    port = -1

    if port_pos == -1 or webserver_pos < port_pos:
        webserver = temp[:webserver_pos]
        port = 80
    else:
        port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
        webserver = temp[:(port_pos)]
    
    return [firstline, webserver, port]
    


if __name__ == '__main__':
    main()

