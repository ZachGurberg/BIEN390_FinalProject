import cv2
import numpy as np

box_threshold = 0
boxes = []


camera=cv2.VideoCapture(0)


camera.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)

lower_bound = np.array([0,100,100])
upper_bound = np.array([30,255,255])

while True:
    ret,frame = camera.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    edges = cv2.Canny(mask, 0, 1000)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:

        x,y,w,h = cv2.boundingRect(cnt)
        if (w>box_threshold and h>box_threshold):
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0),2)
            boxes.append((h,w))

    cv2.imshow('Frame', mask)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
camera.release()

cv2.destroyAllWindows()

print(len(boxes))