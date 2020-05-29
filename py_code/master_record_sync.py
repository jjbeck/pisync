import socket
import time
import sys
import threading
import argparse

# construct the argument parse and parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument("--cn","--camera-number", type=int, default=1, help="number of cameras you are recording from. Sets how many connections master waits for before starting.")
parser.add_argument("--fps","--frames-per-second", type=int, default=30, help="Controls how fast frames are pulled from stream at each camera. Note: Max FPS will be dependent on many factors. Monitor FPS measure on Rasp pi so you can tweak for desired FPS")
parser.add_argument("--port", type=int, default=3000, help="Port to form connection on")
args = parser.parse_args()

# device's IP address
HOST = "0.0.0.0"
PORT = args.port
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
lock = threading.Lock()
conn_len = {0:False,1:False,2:False,3:False}
try:
    s.bind((HOST,PORT))
except socket.error as msg:
    print("Bind failed. Error code:: " + str(msg[0]) + "Message" + msg[1])
    sys.exit(0)
s.listen(10)
cam_connected = 0
cams_avail_record = 0
print("Listening on port: " + str(PORT))

def send_capt_1(conn1,fps):
    while True:
        conn1_capt = conn1.recv(1024).decode()
        if conn1_capt == "cap":
            conn1.send("capture".encode())
        time.sleep(1/fps)
    conn.close()

def send_capt_2(conn1,conn2,fps):
    while True:
        conn1_capt = conn1.recv(1024).decode()
        conn2_capt = conn2.recv(1024).decode()
        if conn1_capt == "cap" and conn2_capt == "cap":
            conn1.send("capture".encode())
            conn2.send("capture".encode())
        time.sleep(1/fps)
    conn.close()

def send_capt_3(conn1,conn2,conn3,fps):
    while True:
        conn1_capt = conn1.recv(1024).decode()
        conn2_capt = conn2.recv(1024).decode()
        conn3_capt = conn3.recv(1024).decode()
        if conn1_capt == "cap" and conn2_capt == "cap" and conn3_capt == "cap":
            conn1.send("capture".encode())
            conn2.send("capture".encode())
            conn3.send("capture".encode())
        time.sleep(1/fps)
    conn.close()

def send_capt_4(conn1,conn2,conn3,conn4,fps):
    while True:
        conn1_capt = conn1.recv(1024).decode()
        conn2_capt = conn2.recv(1024).decode()
        conn3_capt = conn3.recv(1024).decode()
        conn4_capt = conn4.recv(1024).decode()
        if conn1_capt == "cap" and conn2_capt == "cap" and conn3_capt == "cap" and conn4_capt == "cap":
            conn1.send("capture".encode())
            conn2.send("capture".encode())
            conn3.send("capture".encode())
            conn4.send("capture".encode())
        time.sleep(1 / fps)
    conn.close()

while 1:
    conn,addr = s.accept()
    print("Connected")
    cam_connected += 1
    if conn_len[0] == False:
        conn_len[0]=(conn)
    elif conn_len[0] != False and conn_len[1] == False:
        conn_len[1]=(conn)
    elif conn_len[0] != False and conn_len[1] != False and conn_len[2] == False:
        conn_len[2]=(conn)
    elif conn_len[0] != False and conn_len[1] != False and conn_len[2] != False and conn_len[3] == False:
        conn_len[3]=(conn)
    print("Number of cameras connected is {}".format(cam_connected))

    if cam_connected == args.cn:
        for conn in range(0,args.cn):
            try:
                conn_len[conn].send('Starting Capture'.encode())
                cams_avail_record += 1
            except:
                print("Send to Camera failed. Continuing")

        print("Number of cameras connected is {}".format(cams_avail_record))

        if cams_avail_record == 1:
            capt_thread = threading.Thread(target=send_capt_1,args=(conn_len[0],args.fps))
            capt_thread.setDaemon(True)
            capt_thread.start()
        elif cams_avail_record == 2:
            capt_thread = threading.Thread(target=send_capt_2, args=(conn_len[0],conn_len[1], args.fps))
            capt_thread.setDaemon(True)
            capt_thread.start()
        elif cams_avail_record == 3:
            capt_thread = threading.Thread(target=send_capt_3, args=(conn_len[0], conn_len[1],conn_len[2], args.fps))
            capt_thread.setDaemon(True)
            capt_thread.start()
        elif cams_avail_record == 4:
            capt_thread = threading.Thread(target=send_capt_4, args=(conn_len[0], conn_len[1],conn_len[2],conn_len[3], args.fps))
            capt_thread.setDaemon(True)
            capt_thread.start()

s.close()
