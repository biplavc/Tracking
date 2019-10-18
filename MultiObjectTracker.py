#!/usr/bin/python
#
# Copyright 2018 BIG VISION LLC ALL RIGHTS RESERVED
# 

# source: https://www.learnopencv.com/multitracker-multiple-object-tracking-using-opencv-c-python/

# cd /media/biplav/Biplav_2/CollegeStuff/Research/DrReed/AgeofInformation/demo/game/MOTracking/multi-object-tracking/

from __future__ import print_function
import sys
import cv2
from random import randint

trackerTypes = ['BOOSTING', 'MIL', 'KCF','TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

def createTrackerByName(trackerType):
  # Create a tracker based on tracker name
  if trackerType == trackerTypes[0]:
    tracker = cv2.TrackerBoosting_create()
  elif trackerType == trackerTypes[1]: 
    tracker = cv2.TrackerMIL_create()
  elif trackerType == trackerTypes[2]:
    tracker = cv2.TrackerKCF_create()
  elif trackerType == trackerTypes[3]:
    tracker = cv2.TrackerTLD_create()
  elif trackerType == trackerTypes[4]:
    tracker = cv2.TrackerMedianFlow_create()
  elif trackerType == trackerTypes[5]:
    tracker = cv2.TrackerGOTURN_create()
  elif trackerType == trackerTypes[6]:
    tracker = cv2.TrackerMOSSE_create()
  elif trackerType == trackerTypes[7]:
    tracker = cv2.TrackerCSRT_create()
  else:
    tracker = None
    print('Incorrect tracker name')
    print('Available trackers are:')
    for t in trackerTypes:
      print(t)
    
  return tracker

if __name__ == '__main__':

  print("Default tracking algoritm is CSRT \n"
        "Available tracking algorithms are:\n")
  for t in trackerTypes:
      print(t)      

  trackerType = "CSRT"      

  # Set video to load
  videoPath = "videos/Sample.mp4"
  
  # Create a video capture object to read videos
  cap = cv2.VideoCapture(videoPath)
 
  # Read first frame
  success, frame = cap.read()
  # quit if unable to read the video file
  if not success:
    print('Failed to read video')
    sys.exit(1)

  ## Select boxes
  bboxes = []
  colors = [] 

  # OpenCV's selectROI function doesn't work for selecting multiple objects in Python
  # So we will call this function in a loop till we are done selecting all objects
  while True:
    # draw bounding boxes over objects
    # selectROI's default behaviour is to draw box starting from the center
    # when fromCenter is set to false, you can draw box starting from top left corner
    bbox = cv2.selectROI('MultiTracker', frame) # every bbox is an ROI
    bboxes.append(bbox) # bboxes will contain all tracking ROIs
    colors.append((randint(64, 255), randint(64, 255), randint(64, 255))) # give colour to the tracking ROIs
    print("Press q to quit selecting boxes and start tracking")
    print("Press any other key to select next object")
    k = cv2.waitKey(0) & 0xFF
    if (k == 113):  # q is pressed
      break
  
  print('Selected bounding boxes {}'.format(bboxes))

  ## Initialize MultiTracker
  # There are two ways you can initialize multitracker
  # 1. tracker = cv2.MultiTracker("CSRT")
  # All the trackers added to this multitracker
  # will use CSRT algorithm as default
  # 2. tracker = cv2.MultiTracker()
  # No default algorithm specified

  # Initialize MultiTracker with tracking algo
  # Specify tracker type
  
  # Create MultiTracker object
  multiTracker = cv2.MultiTracker_create()

  # Initialize MultiTracker 
  for bbox in bboxes:
    multiTracker.add(createTrackerByName(trackerType), frame, bbox) # for every bounding box created, attach a tracker to each of them
    # this is done on the first frame, so objects that appear later cannot be tracked with this method


  # Process video and track objects
  while cap.isOpened():
    success, frame = cap.read()
    if not success:
      break # when video ends, program stops execution
    
    # get updated location of objects in subsequent frames
    success, boxes = multiTracker.update(frame) # boxes will contain the updated bounding boxes

    # print('boxes')
    # print(type(boxes))
    # print(boxes.shape)
    # so the boxes will be ndarray with shape (m,4) with m = number of objects to be tracked and 4 values for each object that corresponds to left_most_x, left_most_y, width and height of the box


    # draw boundingboxes tracked objects # https://docs.opencv.org/master/dc/da5/tutorial_py_drawing_functions.html


    
    for i, newbox in enumerate(boxes): # 
      p1 = (int(newbox[0]), int(newbox[1]))
      p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
      # to create a rectangle, top-left corner and bottom right corner points are needed. p1 and p2 here.
      cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

      x_center = int(newbox[0] + newbox[2])/2
      y_center = int(newbox[1] + newbox[3])/2

      print("object " + str(i) + " : " )
      print(x_center, y_center)

    # show frame
    cv2.imshow('MultiTracker', frame)
    

    # quit on ESC button
    if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
      break
