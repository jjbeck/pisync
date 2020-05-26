# import the necessary packages
from __future__ import print_function
from image_utils_new_pipe import WebcamVideoStream
from image_utils_new_pipe import FPS
from image_utils_new_pipe import FFMPEG_convert
import argparse
import imutils
import cv2
import subprocess
import socket
import time

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--num-frames", type=int, default=100,
    help="# of frames to loop over for FPS test")

args = vars(ap.parse_args())



#Set up socket and port to listen for connection
BUFFER_SIZE = 1024 
host = '10.9.129.243'
port = 2228
client_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
server_address=(host,port)
client_sock.connect((server_address))




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
while i<24:
    while fps._numFrames < args["num_frames"]:
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
    vs.vid_trans()
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
1) switch pipe for each new video
2) only terminate previous ffmpeg process when old pipe is empty
3) add try and error/exceptions to make code run smoothly
4) implement and spice up video monitor code with cass in separat file like this with args
5) figure out way to encode ffmpeg based on fps
6) add arguments for resolution and fpes for ffmpeg and other aspects of code
"""
