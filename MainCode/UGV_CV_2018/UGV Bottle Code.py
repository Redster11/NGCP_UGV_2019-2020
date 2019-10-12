import numpy as np
import imutils
import argparse
import cv2
import math
import socket
import struct

cap = cv2.VideoCapture(0)
##UDP_IP_ADDRESS = "127.0.0.1"
##UDP_PORT_NO = 6789
##UDP2 = 6790
##UDP3 = 6791


while True:

        _, image = cap.read()
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
        lowh = np.array([103.59712230215827, 0.0, 59.62230215827338])
        upph = np.array([180.0, 111.18686868686868, 255.0])
        output = image.copy()
        mask = cv2.inRange(hsv, lowh, upph)

        
       
        ret,thresh = cv2.threshold(mask, 40, 255, 0)
        
        im2,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        ta = 100
        if len(contours) != 0:
                c = max(contours, key = cv2.contourArea)
                M = cv2.moments(c)
                a = cv2.contourArea(c)
                if a > ta:                        
                        cv2.drawContours(image, c, -1, 255, 3)
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                                                
                        cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)

                        cv2.putText(image, "center", (cX - 20, cY - 20),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                        
                        rows,cols = image.shape[:2]
                        [vx,vy,x,y] = cv2.fitLine(c, cv2.DIST_L2,0,0.01,0.01)
                        left = int((-x*vy/vx) + y)
                        right = int(((cols-x)*vy/vx)+y)
                        image = cv2.line(image,(cols-1,right),(0,left),(0,255,0),2)
                        

                        if(right > cY):
                                anglefound = math.atan2(right-cY, (cols-1) - cX ) * (180/3.141592653589793)
                        else:
                                anglefound = 180 + math.atan2(right-cY, (cols-1) - cX ) * (180/3.141592653589793)
##                        bitboi= bytearray(struct.pack("i", int(anglefound)))
##                        bitboi2 = bytearray(struct.pack("i", int(cX)))
##                        bitboi3 = bytearray(struct.pack("i", int(cY)))
##                       
##                        clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
##                        clientSock.sendto(bitboi, (UDP_IP_ADDRESS, UDP_PORT_NO))
##                        clientSock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
##                        clientSock2.sendto(bitboi2, (UDP_IP_ADDRESS, UDP2))
##                        clientSock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
##                        clientSock3.sendto(bitboi3, (UDP_IP_ADDRESS, UDP3))
                        

                        print('Angle found: ', anglefound)
                        print('Center X coordinate: ', cX)
                        print('Center Y coordinate: ', cY)


                

        
        
        cv2.imshow("mage", image)
        cv2.imshow("mask", mask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
         break

      
cap.release()
cv2.destroyAllWindows()




