#This is the functioning waypoint navigation simulation with keybaord controls.
#You can manually drive the robot with the W,A,S, and D keys.
#Press Q to engage automated waypoint navigation.
#Waypoint navigation can be cancelled at any time by pressing W, A, S, or D.
#The waypoint can be changed by updating the GPSDestination cordinates in the main loop at the bottom. 

from controller import Robot, Motor, DistanceSensor, Camera, Keyboard, GPS, Compass, CameraRecognitionObject
import math

#global variables
global lbMotor, lfMotor, rbMotor, rfMotor, robot, autoPilot, previousKey, headingAdjusted, state

state = 1

#Robot and variable declarations
robot = Robot()
autoPilot = False

gps = robot.getGPS('gps')
gps.enable(250)

compass = robot.getCompass('compass')
compass.enable(250)

camera = robot.getCamera('camera')
camera.enable(100)
camera.recognitionEnable(100)


headingAdjusted = False
previousKey = 61

#function definitions
def initilize_motors(): 
    
    global lbMotor, lfMotor, rbMotor, rfMotor, robot
    lbMotor = robot.getMotor('Motor_LB')
    lfMotor = robot.getMotor('Motor_LF')
    rbMotor = robot.getMotor('Motor_RB')
    rfMotor = robot.getMotor('Motor_RF')
    lbMotor.setPosition(float('inf'))
    lfMotor.setPosition(float('inf'))
    rbMotor.setPosition(float('inf'))
    rfMotor.setPosition(float('inf'))
    
def stop_moving():

    global lbMotor, lfMotor, rbMotor, rfMotor, robot
    lbMotor.setVelocity(0)
    lfMotor.setVelocity(0)
    rbMotor.setVelocity(0)
    rfMotor.setVelocity(0)
    
def move_forward(speed):

    global lbMotor, lfMotor, rbMotor, rfMotor, robotq
    lbMotor.setVelocity(speed)
    lfMotor.setVelocity(speed)
    rbMotor.setVelocity(speed)
    rfMotor.setVelocity(speed)

def move_backward(speed):

    global lbMotor, lfMotor, rbMotor, rfMotor, robot
    lbMotor.setVelocity(-speed)
    lfMotor.setVelocity(-speed)
    rbMotor.setVelocity(-speed)
    rfMotor.setVelocity(-speed)
    
def turn_left(speed):

    global lbMotor, lfMotor, rbMotor, rfMotor, robot
    lbMotor.setVelocity(-speed)
    lfMotor.setVelocity(-speed)
    rbMotor.setVelocity(speed)
    rfMotor.setVelocity(speed)
    
def turn_right(speed):

    global lbMotor, lfMotor, rbMotor, rfMotor, robot
    lbMotor.setVelocity(speed)
    lfMotor.setVelocity(speed)
    rbMotor.setVelocity(-speed)
    rfMotor.setVelocity(-speed)

def read_keyboard_input(key, maxSpeed):
    global autoPilot, previousKey, headingAdjusted
    
    if key == 87:
        move_forward(maxSpeed)
        autoPilot = False
        headingAdjusted = False
    if key == 65:
        turn_left(maxSpeed/5)
        autoPilot = False
        headingAdjusted = False
    if key == 68:
        turn_right(maxSpeed/5)
        autoPilot = False
        headingAdjusted = False
    if key == 83:
        move_backward(maxSpeed)
        autoPilot = False
        headingAdjusted = False
    if key == 81:
        if(key != previousKey): #key can only be pressed once
            autoPilot = not autoPilot
     
    previousKey = key
        
def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")


    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing  

#calculates distance between two GPS cordinates account for curivature of the earth
def haversine(coord1, coord2): 
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))
   
def auto_pilot(maxSpeed, gpsDestination):

    global headingAdjusted, state
    
    heading = 0
    gpsLocation = ()
   

    tempLocation = gps.getValues() #gets 3D GPS location in standard cordinate system
    gpsLocation = (tempLocation[0], -tempLocation[1]) #Converts to 2D and flips cordinate system
                                                      #to match compass
    
    headingVector = compass.getValues() #gets compass heading in vectors
    
    #converts from vectors to degrees. North is zero, rotates through 360 going counterclockwise
    headingDegrees = math.degrees(math.atan2(headingVector[2],headingVector[0]))
    headingDegrees = abs((headingDegrees-360)%360)
    
    targetHeading = calculate_initial_compass_bearing(gpsLocation, gpsDestination)
    targetDistance = haversine(gpsLocation, gpsDestination)
    
    #gets the difference between robot heading and destination heading, converts to 360 degrees
    angleDifference = abs(((headingDegrees - targetHeading)-360)%360)
    
    #turns robot towards gps cordinate and drive forwards
    if(angleDifference <= 180 and headingAdjusted == False):
        turn_right(maxSpeed/5)
    if(angleDifference > 180 and headingAdjusted == False):
       turn_left(maxSpeed/5)
    if(angleDifference < 2 or angleDifference > 358):
        headingAdjusted = True
        
    if(targetDistance>0.2 and headingAdjusted == True):
        move_forward(maxSpeed)
        
    if targetDistance<0.2:
        state = 2
        
def locateAndCenter(maxSpeed):
    objectFound = False
    
    objects = camera.getRecognitionNumberOfObjects()
    recognized = camera.getRecognitionObjects()
    if(objects > 0):
        objectFound = True
    
    if(objectFound == False):
        turn_left(maxSpeed/5)

    if(objectFound):
        objectPosition = recognized[0].get_position_on_image()
        if(objectPosition[0] > 32):
            turn_right(maxSpeed/5)
        elif(objectPosition[0]<29):
            turn_left(maxSpeed/5)
        else:
            state = 3
   

#MAIN
timestep = 64
maxSpeed = -10 #speed is negative because robot is backwards
    
input = robot.getKeyboard()
input.enable(100)    
initilize_motors()



while robot.step(timestep) != -1:
 
    key = input.getKey()
    stop_moving()
    #objectRecognized = False
            
    tempLocation = gps.getValues() #gets 3D GPS location in standard cordinate system
    currentLocation = (tempLocation[0], -tempLocation[1]) #Converts to 2D
    
    headingVector = compass.getValues() #gets compass heading in vectors
    currentHeading = math.degrees(math.atan2(headingVector[2],headingVector[0]))
    currentHeading = abs((currentHeading-360)%360)
    
    gpsDestination = (1.5920715449556217e-05, -1.537514772360986e-05)
    
    if(state == 1):
        auto_pilot(maxSpeed, gpsDestination)
        
    if(state == 2):

        locateAndCenter(maxSpeed)
        
    if(state == 3):
        stop_moving()
        
    #if(key > -1):
       # read_keyboard_input(key,maxSpeed)
    #if(autoPilot == True):
        #auto_pilot(maxSpeed, gpsDestination)
    
    #locateAndCenter(maxSpeed)
    
            
    #uncomment the following line to see location and heading information    
    #print(currentLocation, currentHeading)
       

