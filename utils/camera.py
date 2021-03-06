#!/usr/bin/env python

import cv
import datetime
import os
import math
import time
from random import Random

class Camera:
  HAAR_CASCADE_PATH = "/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml"
  EXTERNAL = True
  CAMERA_INDEX = 1 if EXTERNAL else 0
  LINE_TYPE = cv.CV_AA
  FONT = cv.InitFont(0, 1, 1, 0, 3, LINE_TYPE)
  WHITE = cv.Scalar(255, 255, 255)
  GREEN = cv.Scalar(55, 255, 0)
  RED = cv.Scalar(0, 0, 255)

  def __init__(self):
    cv.NamedWindow("w1", cv.CV_WINDOW_AUTOSIZE)

    self.capture = cv.CaptureFromCAM(Camera.CAMERA_INDEX)
    self.storage = cv.CreateMemStorage()
    self.cascade = cv.Load(Camera.HAAR_CASCADE_PATH)
    self.image = cv.QueryFrame(self.capture)
    self.faces = []

  def detect_faces(self):
    self.faces = []
    detected = cv.HaarDetectObjects(self.image, self.cascade, self.storage, 1.2, 2, cv.CV_HAAR_DO_CANNY_PRUNING, (100,100))
    if detected:
      for (x,y,w,h),n in detected:
        self.faces.append((x,y,w,h))

  def step(self, show):
    r_image = cv.QueryFrame(self.capture)

    if Camera.EXTERNAL:
      self.image = cv.CreateImage((r_image.height, r_image.width), r_image.depth, r_image.channels)
      cv.Transpose(r_image, self.image)
      cv.Flip(self.image, self.image, flipMode=0)
    else:
      self.image = r_image


    self.detect_faces()

    for (x,y,w,h) in self.faces:
      cv.PutText(self.image, "LOOK AT THIS IDIOT", (0, 30), Camera.FONT, Camera.RED)
      cv.PutText(self.image, str(time.time()), (self.image.width - 275, self.image.height - 20), Camera.FONT, Camera.RED)
      cv.Line(self.image, (0, y+h/2), (self.image.width, y+h/2), Camera.RED)
      cv.Line(self.image, (x+w/2, 0), (x+w/2, self.image.height), Camera.RED)
      cv.Circle(self.image, (x+w/2, y+h/2), min(h/2, w/2), Camera.RED, thickness=2)
      cv.Circle(self.image, (x+w/2, y+h/2), min(h/8, w/8), Camera.RED)
      #arrow(self.image, (200, 40), (x, y), Camera.WHITE)

    if show:
      print self.faces
      cv.ShowImage("w1", self.image)
      cv.WaitKey(1)

    return self.image

  def face(self):
    return self.faces

  def save(self):
    name = os.getcwd() + '/images/' + str(datetime.datetime.now()) + '.jpg'
    cv.SaveImage(name, self.image)
    return name

def arrow(img, p1, p2, color):
  denom = p2[0]-p1[0]
  angle = 3*math.pi/2
  if not denom == 0:
    angle = math.atan(float(p2[1]-p1[1])/(p2[0]-p1[0]))
  p2a = (p2[0]-int(10*math.cos(angle+math.pi/4)),
         p2[1]-int(10*math.sin(angle+math.pi/4)))
  p2b = (p2[0]-int(10*math.cos(angle-math.pi/4)),
         p2[1]-int(10*math.sin(angle-math.pi/4)))

  cv.Line(img, p1, p2,  color, 2)
  cv.Line(img, p2a, p2, color, 2)
  cv.Line(img, p2b, p2, color, 2)
