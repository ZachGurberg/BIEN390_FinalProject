import cv2
import numpy as np
import random

def captureVideo():
    filename = "Sample#" + str(random.randint(1,10000))+".avi" 

    #camera parameters
    camera = cv2.VideoCapture(0)
    size = (640,480) #TODO might need to make larger and adjust dependencies in postProcessing/calibration

    #capturing and saving video
    #edge
    if (camera.isOpened() == False): 
        print("Error reading video file")

    result = cv2.videoWriter(filename, cv2.VideoWriter_fourcc(*'MPG'), 10, size)

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
    return filename