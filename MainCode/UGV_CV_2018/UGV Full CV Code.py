import numpy as np
import imutils
import argparse
import cv2
import math
import socket
import struct


maincam = cv2.VideoCapture(0)
UDP_IP_ADDRESS = "127.0.0.1"
udp_reciever = 6800
udp1 = 6789
udp2 = 6790

bottleSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bcenterSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def createtrackbar():
    cv2.namedWindow('UGV Filter')
    cv2.resizeWindow('UGV Filter', 500,500)
    cv2.createTrackbar("MaxHue", "UGV Filter",0,1800,update)
    cv2.createTrackbar("MinHue", "UGV Filter",0,1800,update)
    cv2.createTrackbar("MaxSat", "UGV Filter",0,2550,update)
    cv2.createTrackbar("MinSat", "UGV Filter",0,2550,update)
    cv2.createTrackbar("MaxLum", "UGV Filter",0,2550,update)
    cv2.createTrackbar("MinLum", "UGV Filter",0,2550,update)

def settrackbarvalues(minhue, maxhue, minsat, maxsat, minlum, maxlum):
    cv2.setTrackbarPos("MaxHue", "UGV Filter",maxhue)
    cv2.setTrackbarPos("MinHue", "UGV Filter",minhue)
    cv2.setTrackbarPos("MaxSat", "UGV Filter",maxsat)
    cv2.setTrackbarPos("MinSat", "UGV Filter",minsat)
    cv2.setTrackbarPos("MaxLum", "UGV Filter",maxlum)
    cv2.setTrackbarPos("MinLum", "UGV Filter",minlum)
    


def ballsend(x, y, ballfound, phase):
    ballbyte = bytearray(struct.pack("i", int(x)))
    ballbyte += bytearray(struct.pack("i", int(y)))
    ballbyte += bytearray(struct.pack("i", int(ballfound)))
    bcenterSock.sendto(ballbyte, (UDP_IP_ADDRESS, udp2))
          
    RecieverSock.setblocking(0)
    try:
        data, address = RecieverSock.recvfrom(1024)
        phase = int.from_bytes(data,byteorder='little')
    except socket.error:
        phase = 1

    return phase
        
    
    


def bottlesend(cX, cY, anglefound, bottlefound, phase):
    bottlebyte = bytearray(struct.pack("i", int(anglefound)))
    bottlebyte += (bytearray(struct.pack("i", int(cX))))
    bottlebyte += (bytearray(struct.pack("i", int(cY))))
    bottlebyte += (bytearray(struct.pack("i", int(bottlefound))))
    bottleSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bottleSock.sendto(bottlebyte, (UDP_IP_ADDRESS, udp1))
    print('Angle found: ', anglefound)
    print('Center X coordinate: ', cX)
    print('Center Y coordinate: ', cY)
    
    RecieverSock.setblocking(0)
    try:
        data, address = RecieverSock.recvfrom(1024)
        phase = int.from_bytes(data,byteorder='little')
    except socket.error:
        phase = 2


    return phase



##def bottlesend2(cX, cY, anglefound, bottlefound, phase):
##    bottlebyte = bytearray(struct.pack("i", int(anglefound)))
##    bottlebyte += (bytearray(struct.pack("i", int(cX))))
##    bottlebyte += (bytearray(struct.pack("i", int(cY))))
##    bottlebyte += (bytearray(struct.pack("i", int(bottlefound))))
##    bottleSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
##    bottleSock.sendto(bottlebyte, (UDP_IP_ADDRESS, udp1))
##    print('Angle found: ', anglefound)
##    print('Center X coordinate: ', cX)
##    print('Center Y coordinate: ', cY)
##    
##    RecieverSock.setblocking(0)
##    try:
##        data, address = RecieverSock.recvfrom(1024)
##        phase = int.from_bytes(data,byteorder='little')
##    except socket.error:
##        phase = 3
##
##
##    return phase
    


def update(x):
    pass




RecieverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
RecieverSock.bind((UDP_IP_ADDRESS, udp_reciever))
data, address = RecieverSock.recvfrom(1024)
phase = int.from_bytes(data,byteorder='little')

createtrackbar()


# settrackbarvalues(minhue, maxhue, minsat, maxsat, minlum, maxlum):

## 1:30 PM No clouds (Pomona) Bright Red Values
##settrackbarvalues(1709, 1800, 1096, 2550, 76, 2474)

## AirBnb Filter
settrackbarvalues(1166,1800, 609, 2550, 540, 2550)


x = 0
y = 0
ballfound = 0
ta = 200

counter = 0
while phase == 1:

    
    _, image = maincam.read()

    
    output = image.copy()
    hsl = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    maxhue =(cv2.getTrackbarPos("MaxHue", "UGV Filter"))/10
    minhue = (cv2.getTrackbarPos("MinHue", "UGV Filter"))/10
    maxsat=(cv2.getTrackbarPos("MaxSat", "UGV Filter"))/10
    minsat=(cv2.getTrackbarPos("MinSat", "UGV Filter"))/10
    maxlum=(cv2.getTrackbarPos("MaxLum", "UGV Filter"))/10
    minlum=(cv2.getTrackbarPos("MinLum", "UGV Filter"))/10
    
    lowh = np.array([minhue, minlum, minsat])
    upph = np.array([maxhue, maxlum, maxsat])

    ## 1:30 PM No clouds (Pomona) Dark Red Values
    lowh2 = np.array([124.7, 12.2, 152.2])
    upph2 = np.array([180.0, 47.2, 197.1])
    
    
    mask = cv2.inRange(hsl, lowh, upph)
    mask2 = cv2.inRange(hsl, lowh2, upph2)
    total = cv2.add(mask, mask2)
    
    

    ret,thresh = cv2.threshold(mask, 40, 255, 0)
    im2,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
      
    if counter == 0:
        ballfound = 0
        
        

    if len(contours) != 0:
        c = max(contours, key = cv2.contourArea)
        M = cv2.moments(c)
        a = cv2.contourArea(c)
        if a > ta:
            if counter == 5:                     
                ballfound =  1

            cv2.drawContours(output, c, -1, (0, 0, 255), 3)
            x = int(M["m10"] / M["m00"])
            y = int(M["m01"] / M["m00"])
                                                
            cv2.circle(output, (x, y), 7, (255, 255, 255), -1)

            cv2.putText(output, "center", (x - 20, y - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            if ta < 500:
                ta = ta + 4
            if counter < 5:
                counter = counter + 1
        
    
            cv2.imshow('mask', total)
            cv2.imshow('image',output)

            phase = ballsend(x, y, ballfound, phase)

                   
            if cv2.waitKey(1) & 0xFF == ord('q'):
                maincam.release()
                cv2.destroyAllWindows()
                break

            continue
        
        else:
            counter = 0
            ta = 200
            ballfound = 0

            cv2.imshow('mask', total)
            cv2.imshow('image',output)

            phase = ballsend(x, y, ballfound, phase)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                maincam.release()
                cv2.destroyAllWindows()
                break

            continue
        
    cv2.imshow('mask', total)
    cv2.imshow('image',output)
    ta = 200
    phase = ballsend(x, y, ballfound, phase)
    

    if cv2.waitKey(1) & 0xFF == ord('q'):
        maincam.release()
        cv2.destroyAllWindows()
        break


cv2.destroyAllWindows()

createtrackbar()
# settrackbarvalues(minhue, maxhue, minsat, maxsat, minlum, maxlum):

# initial values inside lighting 
settrackbarvalues(177, 387, 1050, 2550, 579, 2093)





ta = 100

counter = 0

anglefound = 0
cX = 0
cY = 0

while phase==2:

    _, image = maincam.read()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    maxhue =(cv2.getTrackbarPos("MaxHue", "UGV Filter"))/10
    minhue = (cv2.getTrackbarPos("MinHue", "UGV Filter"))/10
    maxsat=(cv2.getTrackbarPos("MaxSat", "UGV Filter"))/10
    minsat=(cv2.getTrackbarPos("MinSat", "UGV Filter"))/10
    maxlum=(cv2.getTrackbarPos("MaxLum", "UGV Filter"))/10
    minlum=(cv2.getTrackbarPos("MinLum", "UGV Filter"))/10

    lowh = np.array([minhue, minlum, minsat])
    upph = np.array([maxhue, maxlum, maxsat])
    

    output = image.copy()
    mask = cv2.inRange(hsv, lowh, upph)

    
   
    ret,thresh = cv2.threshold(mask, 40, 255, 0)
    
    im2,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if ta < 200:
        ta = ta + 10

   
    if counter == 0:
        bottlefound = 0
    
    

    if len(contours) != 0:
            c = max(contours, key = cv2.contourArea)
            M = cv2.moments(c)
            a = cv2.contourArea(c)
            if a > ta:
                if counter == 5:                     
                    bottlefound =  1
                  
                cv2.drawContours(image, c, -1,(0, 255, 255), 3)
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

                if counter < 5:
                    counter = counter + 1

                
                cv2.imshow("image", image)
                cv2.imshow("mask", mask)

                phase = bottlesend(cX, cY, anglefound, bottlefound,phase)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    maincam.release()
                    cv2.destroyAllWindows()
                    break
                
                continue
                
            else:
                cv2.imshow("image", image)
                cv2.imshow("mask", mask)
                counter = 0
                bottlefound = 0
                phase = bottlesend(cX, cY, anglefound, bottlefound, phase)


                if cv2.waitKey(1) & 0xFF == ord('q'):
                    maincam.release()
                    cv2.destroyAllWindows()
                    break
            
                continue
            
    cv2.imshow("image", image)
    cv2.imshow("mask", mask)
    phase = bottlesend(cX, cY, anglefound, bottlefound,phase)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        maincam.release()
        cv2.destroyAllWindows()
        break


maincam.release()
cv2.destroyAllWindows()



##createtrackbar()
##
##armcam = cv2.VideoCapture(1)
### settrackbarvalues(minhue, maxhue, minsat, maxsat, minlum, maxlum):
##
### initial values inside lighting 
##settrackbarvalues(161, 360, 2078, 2550, 510,  2352)
##
##ta = 100
##
##counter = 0
##
##anglefound = 0
##cX = 0
##cY = 0
##
##
##
##while phase == 3:
##    _, image = armcam.read()
##    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
##    maxhue =(cv2.getTrackbarPos("MaxHue", "UGV Filter"))/10
##    minhue = (cv2.getTrackbarPos("MinHue", "UGV Filter"))/10
##    maxsat=(cv2.getTrackbarPos("MaxSat", "UGV Filter"))/10
##    minsat=(cv2.getTrackbarPos("MinSat", "UGV Filter"))/10
##    maxlum=(cv2.getTrackbarPos("MaxLum", "UGV Filter"))/10
##    minlum=(cv2.getTrackbarPos("MinLum", "UGV Filter"))/10
##
##    lowh = np.array([minhue, minlum, minsat])
##    upph = np.array([maxhue, maxlum, maxsat])
##    
##
##    output = image.copy()
##    mask = cv2.inRange(hsv, lowh, upph)
##
##    
##   
##    ret,thresh = cv2.threshold(mask, 40, 255, 0)
##    
##    im2,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
##
##    if ta < 200:
##        ta = ta + 10
##
##   
##    if counter == 0:
##        bottlefound = 0
##    
##    
##
##    if len(contours) != 0:
##            c = max(contours, key = cv2.contourArea)
##            M = cv2.moments(c)
##            a = cv2.contourArea(c)
##            if a > ta:
##                    if counter == 5:                     
##                        bottlefound =  1
##                      
##                    cv2.drawContours(image, c, -1,(0, 255, 255), 3)
##                    cX = int(M["m10"] / M["m00"])
##                    cY = int(M["m01"] / M["m00"])
##                                            
##                    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
##
##                    cv2.putText(image, "center", (cX - 20, cY - 20),
##                                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
##                    
##                    rows,cols = image.shape[:2]
##                    [vx,vy,x,y] = cv2.fitLine(c, cv2.DIST_L2,0,0.01,0.01)
##                    left = int((-x*vy/vx) + y)
##                    right = int(((cols-x)*vy/vx)+y)
##                    image = cv2.line(image,(cols-1,right),(0,left),(0,255,0),2)
##
##                    if(right > cY):
##                            anglefound = math.atan2(right-cY, (cols-1) - cX ) * (180/3.141592653589793)
##                    else:
##                            anglefound = 180 + math.atan2(right-cY, (cols-1) - cX ) * (180/3.141592653589793)
##
##                    if counter < 5:
##                        counter = counter + 1
##
##                    
##                    cv2.imshow("image", image)
##                    cv2.imshow("mask", mask)
##
##                    phase = bottlesend2(cX, cY, anglefound, bottlefound,phase)
##
##                    if cv2.waitKey(1) & 0xFF == ord('q'):
##                        maincam.release()
##                        cv2.destroyAllWindows()
##                        break
##                    
##                    continue
##                    
##            else:
##                cv2.imshow("image", image)
##                cv2.imshow("mask", mask)
##                counter = 0
##                bottlefound = 0
##                phase = bottlesend2(cX, cY, anglefound, bottlefound,phase)
##
##                if cv2.waitKey(1) & 0xFF == ord('q'):
##                    maincam.release()
##                    cv2.destroyAllWindows()
##                    break
##                
##                continue
##            
##    cv2.imshow("image", image)
##    cv2.imshow("mask", mask)
##    phase = bottlesend2(cX, cY, anglefound, bottlefound,phase)
##    
##    if cv2.waitKey(1) & 0xFF == ord('q'):
##        maincam.release()
##        cv2.destroyAllWindows()
##        break
##    
##
##armcam.release()
##cv2.destroyAllWindows() 

