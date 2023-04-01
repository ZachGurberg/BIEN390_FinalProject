import cv2
import numpy as np
from VideoCapture import VideoRecorder


def GetData(showVideo):
    # filename = captureVideo()
    # cap = cv2.VideoCapture(filename) ##should set to this, for testing we will use the sample

    cap = cv2.VideoCapture("test.avi")

    #box parameters
    box_threshold = 5
    boxes = [] 

    #threshold for HSV color space (targetted to red)
    lower_bound = np.array([0,30,30])
    upper_bound = np.array([90,255,255])

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            edges = cv2.Canny(mask, 0, 1000)
            contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            for cnt in contours:
                x, y, w, h = cv2.boundingRect(cnt)
                if (w > box_threshold and h > box_threshold):
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    boxes.append((h,w))
            if (showVideo):
                cv2.imshow('Processed Frame', frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
        else:
            break

    #convert to volumes
    tuples_array = np.array(boxes)
    volumes = tuples_array[:,0]*tuples_array[:,1]
    return volumes