# import the necessary packages
import datetime
from threading import Thread
import cv2
import subprocess

class FPS:
    def __init__(self):
        # store the start time, end time, and total number of frames
        # that were examined between the start and end intervals
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        # start the timer
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        # stop the timer
        self._end = datetime.datetime.now()

    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._numFrames += 1

    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval
        return (self._end - self._start).total_seconds()

    def fps(self):
        # compute the (approximate) frames per second
        return self._numFrames / self.elapsed()
    
class FFMPEG_convert:
    def __init__(self):
        self.dtime = datetime.datetime.now()
        self.month = self.dtime.month
        self.day = self.dtime.day
        self.hour = self.dtime.hour
        self.minute = self.dtime.minute
        self.second = self.dtime.second
        self.filename = '/home/pi/Desktop/Mouse.{}.{}.{}.{}.{}_cam1.h264'.format(self.month,self.day,self.hour,self.minute,self.second)
        self.command = ['ffmpeg',
            '-f', 'rawvideo',
            '-pix_fmt', 'bgr24',
            '-s','1280x720',
            '-i','-', '-v', '-1',
            '-strict','experimental',
            '-vcodec','h264',
            '-pix_fmt','yuv420p',
            '-vb','1000k',
            '-profile:v', 'baseline',
            '-preset', 'ultrafast',
            '-r', '40',
            '-f', 'flv', 
            self.filename]
        
        self.pipe = subprocess.Popen(self.command, stdin=subprocess.PIPE)
        
    def stop(self):
        self.pipe.kill()
        


class WebcamVideoStream(FFMPEG_convert):
    def __init__(self, fconv, src=0, name="WebcamVideoStream"):
        self.pipe = fconv.pipe
        self.filename = fconv.filename
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)


        (self.grabbed, self.frame) = self.stream.read()

        # initialize the thread name
        self.name = name

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self
    
    def new_video(self):
        #register time metrics
        self.dtime = datetime.datetime.now()
        self.month = self.dtime.month
        self.day = self.dtime.day
        self.hour = self.dtime.hour
        self.minute = self.dtime.minute
        self.second = self.dtime.second
        self.filename = '/home/pi/Desktop/Mouse.{}.{}.{}.{}.{}_cam1.h264'.format(self.month,self.day,self.hour,self.minute,self.second)
        self.command = ['ffmpeg',
            '-f', 'rawvideo',
            '-pix_fmt', 'bgr24',
            '-s','1280x720',
            '-i','-', '-v', '-1',
            '-strict','experimental',
            '-vcodec','h264',
            '-pix_fmt','yuv420p',
            '-vb','1000k',
            '-profile:v', 'baseline',
            '-preset', 'ultrafast',
            '-r', '40',
            '-f', 'flv', 
            self.filename]
        #stop previous process
        self.stop()
        #start new
        self.pipe = subprocess.Popen(self.command, stdin=subprocess.PIPE)
        
    def vid_trans(self):
        subprocess.call("rsync" + " " + "--remove-source-files" + " " + self.filename + " "  + "ccv:/users/jbecke11/data/jbecke11/nih_mice_beh/videos", shell = True)

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        self.pipe.stdin.write(self.frame.tostring())
        

    def stop(self):
        # indicate that the thread should be stopped
        self.pipe.kill()
        self.stopped = True
        
        
