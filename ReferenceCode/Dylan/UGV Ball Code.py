# import the necessary packages
import numpy as np
import argparse
import cv2
import time

cap = cv2.VideoCapture(0) 



while(True):
	# Capture frame-by-frame
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    lowh = np.array([0, 156, 138])
    upph = np.array([65, 255, 255])
    mask = cv2.inRange(hsv, lowh, upph)
    edges = cv2.Canny(mask,150,200)
    ret,thresh = cv2.threshold(mask, 40, 255, 0)
	# load the image, clone it for output, and then convert it to grayscale
			
    radius = 24.324324324324326
    ksize = int(6 * round(radius) + 1)
    output = frame.copy()
  
    res2=cv2.GaussianBlur(thresh,(ksize, ksize), round(radius))
	
	
	# detect circles in the image
    circles = cv2.HoughCircles(res2, cv2.HOUGH_GRADIENT, 1, 200, param1=30, param2=35, minRadius=0, maxRadius=0)
	# print circles
	
	# ensure at least some circles were found
    if circles is not None:
		# convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
		
	# loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            cv2.circle(output, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
	    #time.sleep(0.5)
            print ("X coordinate:")
            print (x)
            print ("Y coordinate: ")
            print (y)
            print ("Radius is: ")
            print (r)



    cv2.imshow('gray',res2)
    cv2.imshow('frame',output)
    if cv2.waitKey(1) & 0xFF == ord('q'):
         break


	
# When everything done, release the capture

cap.release()
cv2.destroyAllWindows()
