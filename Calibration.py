import cv2
import numpy as np
from Legacy.VideoCapture import VideoRecorder


def Calibration(known_h, known_w):
    light_blue_lower = (35, 50, 50)
    light_blue_upper = (70, 255, 255)
    
    # define the known height to width ratio of the object
    known_ratio = known_h/known_w
    
    pixel_to_cm_factor = None

    # initialize the camera
    cap = cv2.VideoCapture(0)
    
    width_mean = []
    height_mean = []

    while cap.isOpened():
        # capture a frame from the camera
        ret, frame = cap.read()

        # convert the frame from BGR to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # create a mask for the object color
        mask = cv2.inRange(hsv_frame, light_blue_lower, light_blue_upper)

        # apply a median blur to reduce noise
        mask = cv2.medianBlur(mask, 5)

        # detect edges using the Canny edge detection algorithm
        edges = cv2.Canny(mask, 100, 200)

        # find contours in the edges
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # loop through the contours and find the rectangle with the largest area
        max_area = 0
        max_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                max_contour = contour

        # if a rectangle is found and it has the same height to width ratio as the known object, calculate the pixel to cm factor and break
        if max_contour is not None:
            x, y, w, h = cv2.boundingRect(max_contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            current_ratio = h / w
#             print(len(height_mean), len(width_mean))
            if abs(current_ratio - known_ratio) < 0.1:
                height_mean.append(h)
                width_mean.append(w)
                if len(height_mean) >= 30:
                    pixel_to_cm_factor = np.average(((known_w / np.array(width_mean)) + (known_h / np.array(height_mean))))/2 
                    break
            else:
                height_mean.clear()
                width_mean.clear()
        # display the frame
        cv2.imshow('Calibration', frame)
        # exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()
    showMessage('Calibration Complete', 1000)
    return pixel_to_cm_factor

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
    test = Calibration(0.5, 5.5)
    print(test)