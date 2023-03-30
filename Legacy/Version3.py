import cv2
import numpy as np

#parameters for the output bounding boxes we aim to capture
box_threshold = 0
boxes = [] 

#camera parameters
camera = cv2.VideoCapture(0)
size = (640,480)

#capturing and saving video
#edge
if (camera.isOpened() == False): 
    print("Error reading video file")

result = cv2.videoWriter('filename.avi', cv2.VideoWriter_fourcc(*'MPG'), 10, size)

while(True):
    ret, frame = camera.read()
  
    if ret == True: 
  
        # Write the frame into the
        # file 'filename.avi'
        result.write(frame)
  
        # Display the frame
        # saved in the file
        cv2.imshow('Frame', frame)
  
        # Press S on keyboard 
        # to stop the process
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
  
    # Break the loop
    else:
        break

camera.release()
result.release()