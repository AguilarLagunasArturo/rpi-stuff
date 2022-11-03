# import the necessary packages
from flask import Flask, render_template_string, Response
from cv_recon import cv_tools
from time import sleep
import numpy as np
import cv2 as cv
import threading
import socket

''' Video Recording '''
# initialize the camera
cam = cv.VideoCapture(0)
# allow the camera to warmup
sleep(2.0)
# capture frames from the camera
while True:
    _, frame = cam.read()
    cv.imshow('grid', frame)
    #if not update: update = True
    if cv.waitKey(1) & 0xFF == ord("q"):
        break
cam.release()
cv.destroyAllWindows()
