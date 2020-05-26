import socket
import time
import sys
import threading

# device's IP address
HOST = "0.0.0.0"
PORT = 2228
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
lock = threading.Lock()
conn_len = []
try:
    s.bind((HOST,PORT))
except socket.error as msg:
    print("Bind failed. Error code:: " + str(msg[0]) + "Message" + msg[1])
    sys.exit(0)

s.listen(5)
print("Listening on port: " + str(PORT))


def send_capt(conn,conn1,fps):
    while True:
        conn_capt = conn.recv(1024).decode()
        conn1_capt = conn1.recv(1024).decode()
        if conn_capt == "cap" and conn1_capt == "cap":
            conn.send("capture".encode())
            conn1.send("capture".encode())


        time.sleep(1/fps)

    conn.close()


while 1:
    conn,addr = s.accept()
    print("Connected")
    conn_len.append(conn)

    if len(conn_len) == 2:
        conn_len[0].send('Starting Capture'.encode())
        conn_len[1].send('Starting Capture'.encode())
        capt_thread = threading.Thread(target=send_capt,args=(conn_len[0],conn_len[1],300))
        #rec_thread = threading.Thread(target=send_receive, ags=(conn_len[0],conn_len[1]))
        #rec_thread.setDaemon(True)
        #rec_thread.start()
        capt_thread.setDaemon(True)
        capt_thread.start()

s.close()

"""
# receive 4096 bytes each time
BUFFER_SIZE = 1024


# create the server socket
# TCP socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# bind the socket to our local address
s.connect((HOST,PORT))

# enabling our server to accept connections
# 5 here is the number of unaccepted connections that
# the system will allow before refusing new connections
frame = 1
time.sleep(2)
t=time.time()

while True:
    # receive using client socket, not server socket
    s.send("capture".encode())
    time.sleep(1/60)

    frame+=1
stop = time.time()
print("elapsed time is {}".format(60/(stop-t)))
# close the client socket

# close the server socket
s.close()
"""