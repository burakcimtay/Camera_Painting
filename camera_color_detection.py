import cv2
import numpy as np

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,100)

def empty(a):
    pass

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 179, 179, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

while True:
    _, img= cap.read()
    imgHSV=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    hue_min=cv2.getTrackbarPos("Hue Min", "TrackBars")
    hue_max=cv2.getTrackbarPos("Hue Max", "TrackBars")
    
    sat_min=cv2.getTrackbarPos("Sat Min", "TrackBars")
    sat_max=cv2.getTrackbarPos("Sat Max", "TrackBars")
    
    val_min=cv2.getTrackbarPos("Val Min", "TrackBars")
    val_max=cv2.getTrackbarPos("Val Max", "TrackBars")
    
    print(hue_min,hue_max,sat_min,sat_max,val_min,val_max)
    
    lower=np.array([hue_min, sat_min, val_min])
    upper=np.array([hue_max, sat_max, val_max])
    final_mask=cv2.inRange(imgHSV, lower, upper)
    imgResult=cv2.bitwise_and(img, img, mask=final_mask)
    
    final_mask=cv2.cvtColor(final_mask, cv2.COLOR_GRAY2BGR)
    stack=np.hstack([img, final_mask, imgResult])
    stack = cv2.flip(stack,1)
    cv2.imshow("Camera-Segmentation-Result", stack)
    
    if cv2.waitKey(1) & 0xFF==ord("q"):
        break
    
cap.release()
cv2.destroyAllWindows()