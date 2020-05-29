# import the necessary packages
from __future__ import print_function
from recording_utils import WebcamVideoStream
from recording_utils import FPS
from recording_utils import FFMPEG_convert
import argparse
import sys
import cv2
import socket

# construct the argument parse and parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument("--n", "--num-frames", type=int, default=100,
    help="# of frames to loop over for FPS test")
parser.add_argument("--ip", "--ip4",help = "ip4 address to connect to master")
parser.add_argument("--hr","--hours-to-record", type=int, default=24, help="number of hours to record")
parser.add_argument("--tl","--transfer-location",help="hostname and location (ssh) to transfer video. Make sure you have set,"
                                                      "up keygen before running")
args = parser.parse_args()

#Set up socket and port to listen for connection
BUFFER_SIZE = 1024 
host = args.ip
port = 2228
client_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
server_address=(host,port)

try:
    client_sock.connect((server_address))
except socket.error as msg:
    print("Couldnt connect with the socket-server: %s\n terminating program" % msg)
    print("Double check port and ip4 address")
    sys.exit(1)


#waits for number of camera's to connect and then triggers recording
# created a *threaded* video stream, allow the camera sensor to warmup,
# and start the FPS counter
while True:
    if client_sock.recv(BUFFER_SIZE).decode() == "Starting Capture":
        break
# loop over some frames...this time using the threaded stream


print("[INFO] sampling THREADED frames from webcam...")
vs = WebcamVideoStream(fconv=FFMPEG_convert(),src=0).start()
fps = FPS()
fm = FFMPEG_convert()
i = 0
fps.start()
client_sock.send("cap".encode())
while i<args.hr:
    while fps._numFrames < args.n:
        # grab the frame from the threaded video stream and resize it
        # to have a maximum width of 400 pixels
        if client_sock.recv(BUFFER_SIZE).decode() == "capture":

            vs.read()
            
        # update the FPS counter
            fps.update()
        client_sock.send("cap".encode())
        

    # stop the timer and display FPS information

    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
    fps = FPS()
    vs.vid_trans(args.tl)
    i+=1
    fps.start()
    
    #time.sleep(3)
    
    vs.new_video()
# do a bit of cleanup and close everything
fm.stop()
cv2.destroyAllWindows()
vs.stop()

"""
Nest steps:
1) add arument on master for number of cameras
2) tst code so far and then continue
3) add try and error/exceptions to make code run smoothly
6) add arguments for resolution and fpes for ffmpeg and other aspects of code
"""
