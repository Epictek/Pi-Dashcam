#!/usr/bin/python

import picamera
import datetime as dt
import signal
import time
import sys
import os
import thread

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def RunCamera(argv, killer):
  vid_len = 60
  with picamera.PiCamera() as camera:
    camera.resolution = (1360, 768)
    camera.framerate = 24
    camera.brightness = 60
    camera.contrast = 20
    camera.sharpness = 20
    camera.iso = 0
    camera.annotate_foreground = picamera.Color('black')
    camera.annotate_background = picamera.Color('white')
    camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    camera.annotate_text_size = 22
    zero = dt.datetime.now()
    while True:
      start = dt.datetime.now()
      file_name = start.strftime('/home/pi/videos/frontcam/%Y%m%d-%H%M%S.h264')
      print 'Record: ' + file_name
      camera.start_recording(file_name, bitrate=4500000)
      now = dt.datetime.now()
      while (now - start).seconds <= vid_len:
        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.wait_recording(1)
        now = dt.datetime.now()
        if killer.kill_now:
            camera.stop_recording()
            break
      camera.stop_recording()

if __name__ == "__main__":
    killer = GracefulKiller()
    make_sure_path_exists('/home/pi/videos/frontcam')
    RunCamera(sys.argv, killer)