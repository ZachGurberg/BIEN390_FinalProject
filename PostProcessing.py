import cv2
import numpy as np
from Legacy.VideoCapture import VideoRecorder


def GetData(filename, showVideo):
    pause = False
    # filename = captureVideo()
    # cap = cv2.VideoCapture(filename) ##should set to this, for testing we will use the sample

    cap = cv2.VideoCapture(filename)

    #box parameters
    box_threshold = 0
    boxes = [] 

    #thresholding out white
    lower_bound = np.array([0,30,30])
    upper_bound = np.array([255,255,255])

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            edges = cv2.Canny(mask, 0, 1000)
            contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            for cnt in contours:

                #Approach 1: regular bounding rectangle
                # x, y, w, h = cv2.boundingRect(cnt)
                # if (w > box_threshold and h > box_threshold):
                #     cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                #     boxes.append((h,w))
                #     pause = True

                #Approach 2: Ellipse
                area = cv2.contourArea(cnt)
                if area > box_threshold:
                    ellipse = cv2.fitEllipse(cnt)
                    cv2.ellipse(frame, ellipse, (0, 255, 0), 2)
                    center, axes, angle = ellipse
                    major_axis = max(axes)
                    minor_axis = min(axes)
                    pause = True

                #Approach 3: Minimum Area Rectangle Rotated
                # area = cv2.contourArea(cnt)
                # if area > box_threshold:
                #     rect = cv2.minAreaRect(cnt)
                #     box = cv2.boxPoints(rect)
                #     box = np.int0(box)
                #     cv2.drawContours(frame,[box],0,(0,255,0),2)
                #     width, height = rect[1]
                #     boxes.append((width, height))
                #     pause = True
            if (showVideo):
                cv2.imshow('Processed Frame', frame)
                while pause:
                    key = cv2.waitKey(0)
                    if (key == ord('y')):
                        showMessage('Frame Saved', 1000)
                        boxes.append((major_axis, minor_axis))
                        pause = False
                    elif (key == ord('n')):
                        showMessage('Frame Discarded', 1000)
                        pause = False
                    else:
                        showMessage('Invalid Input', 1000)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
        else:
            cv2.destroyAllWindows()
            break

    #convert to volumes
    tuples_array = np.array(boxes)
    volumes = (4*np.pi/3)*tuples_array[:,0]*tuples_array[:,1]*tuples_array[:,1] #Assume depth axis is minor axis 4π/3abc, b=c
    return volumes

def showMessage(message, time):
    # create an image to display the message on
    img = np.zeros((512, 512, 3), np.uint8)
    # add the text to the image
    cv2.putText(img, message, (100, 256), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # display the image for time
    cv2.imshow('Message', img)
    cv2.waitKey(time)
    # close the window
    cv2.destroyAllWindows()


if __name__ == "__main__":
    volumes = GetData("test.avi", True)
    print(volumes)
