import cv2
import numpy as np

MAX_DISTANCE = 190
box_threshold = 5000 #If want to use the optimize contours, set this to 3000 and unhastag lines 87-128

def GetData(filename, showVideo):
    pause = False
    # filename = captureVideo()
    # cap = cv2.VideoCapture(filename) ##should set to this, for testing we will use the sample

    cap = cv2.VideoCapture(filename)

    #box parameters
    boxes = [] 

    #thresholding out white
#     lower_bound = np.array([60, 100, 100]) #These one were done in class 04/13
#     upper_bound = np.array([170, 255, 255])

#     lower_bound = np.array([60, 59, 100])
    lower_bound = np.array([55,59,90])
    upper_bound = np.array([255,255,255])

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            kernel = np.ones((5,5),np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

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
                cv2.imshow('Processed Frame', cv2.resize(mask, (600,480)))
                cv2.imshow('Native', cv2.resize(frame, (600,480)))
                while pause:
                    key = cv2.waitKey(0)
                    if (key == ord('y')):
                        showMessage('Frame Saved', 1000)
                        boxes.append((major_axis, minor_axis))
                        pause = False
                    elif (key == ord('n')):
                        showMessage('Frame Discarded', 1000)
                        pause = False
                    elif (key == ord('q')):
                        break
                    else:
                        showMessage('Invalid Input', 1000)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
        else:
            cv2.destroyAllWindows()
            break
         
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if ret:
#             hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#             mask = cv2.inRange(hsv, lower_bound, upper_bound)
#             kernel = np.ones((5,5),np.uint8)
#             mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
#             mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
# 
#             edges = cv2.Canny(mask, 0, 1000)
#             contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#             contours, hierarchy = optimize_contours(frame, contours, hierarchy)
#             for cnt in contours:
#                 area = cv2.contourArea(cnt)
#                 if area > box_threshold:
#                     ellipse = cv2.fitEllipse(cnt)
#                     cv2.ellipse(frame, ellipse, (0, 255, 0), 2)
#                     center, axes, angle = ellipse
#                     major_axis = max(axes)
#                     minor_axis = min(axes)
#                     pause = True
#             if (showVideo):
#                 cv2.imshow('Processed Frame', cv2.resize(mask, (600,480)))
#                 cv2.imshow('Native', cv2.resize(frame, (600,480)))
#                 while pause:
#                     key = cv2.waitKey(0)
#                     if (key == ord('y')):
#                         showMessage('Frame Saved', 1000)
#                         boxes.append((major_axis, minor_axis))
#                         pause = False
#                     elif (key == ord('n')):
#                         showMessage('Frame Discarded', 1000)
#                         pause = False
#                     elif (key == ord('q')):
#                         break
#                     else:
#                         showMessage('Invalid Input', 1000)
#                 if cv2.waitKey(25) & 0xFF == ord('q'):
#                     break
#         else:
#             cv2.destroyAllWindows()
#             break

    #convert to volumes
    tuples_array = np.array(boxes)
    volumes = (4*np.pi/3)*tuples_array[:,0]*tuples_array[:,1]*tuples_array[:,1] #Assume depth axis is minor axis 4π/3abc, b=c
    print(volumes)
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

def check_overlap(contour1, contour2):
    """Check if two contours overlap within a specified distance."""
    M1 = cv2.moments(contour1)
    M2 = cv2.moments(contour2)
    box_threshold_2 = 200
    try:
    # Calculate the centers of mass of the contours
        if (cv2.contourArea(contour1) > box_threshold or cv2.contourArea(contour2) > box_threshold)\
           and cv2.contourArea(contour1) > box_threshold_2 and cv2.contourArea(contour2) > box_threshold_2:
            hull1 = cv2.convexHull(contour1)
            hull2 = cv2.convexHull(contour2)
            # Get the extreme points of the convex hulls
            ext1 = tuple(hull1[hull1[:, :, 1].argmin()][0])
            ext2 = tuple(hull2[hull2[:, :, 1].argmin()][0])
            
            # Calculate the distance between the extreme points
            dist = np.sqrt((ext2[0] - ext1[0])**2 + (ext2[1] - ext1[1])**2)

            print(ext1, ext2, dist)
            # If the distance between the extreme points is less than the maximum allowed distance,
            # then the contours overlap
            if dist < MAX_DISTANCE:
                return True
            else:
                return False
    except ZeroDivisionError:
        return False

def optimize_contours(frame, contours, hierarchy):
    """Optimize contours by merging overlapping contours."""
    merged_contours = []
    merged_hierarchy = []
    to_merge = []
    for i in range(len(contours)):
        # Only consider contours that are not already marked for merging
        if i not in to_merge:
            merged_contour, to_merge = merge_overlapping_contours(contours[i], contours, hierarchy, to_merge)
            merged_contours.append(merged_contour)
            merged_hierarchy.append(hierarchy[0][i])

    return merged_contours, np.array([merged_hierarchy], dtype=np.int32)


def merge_overlapping_contours(contour, contours, hierarchy, to_merge):
    """Recursive function to merge overlapping contours."""
    merged_contour = contour
    for i in range(len(contours)):
        # Only consider contours that are not already marked for merging
        if i not in to_merge:
            if check_overlap(contour, contours[i]):
                # Merge overlapping contour into the merged contour
                merged_contour = np.vstack((merged_contour, contours[i]))
                to_merge.append(i)
                # Recursively merge overlapping contours of the merged contour
                merged_contour, to_merge = merge_overlapping_contours(merged_contour, contours, hierarchy, to_merge)

    return merged_contour, to_merge
if __name__ == "__main__":
    volumes = GetData("Crop.MP4", True)
#     print(volumes)
