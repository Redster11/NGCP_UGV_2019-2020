from controller import Robot, Motor, DistanceSensor, Camera, Keyboard, GPS, Compass
import math

#global variables
global lbMotor, lfMotor, rbMotor, rfMotor, robot

robot = Robot()

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

    global lbMotor, lfMotor, rbMotor, rfMotor, robot
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
    if key == 87:
        move_forward(maxSpeed)
    if key == 65:
        turn_left(maxSpeed/2)
    if key == 68:
        turn_right(maxSpeed/2)
    if key == 83:
        move_backward(maxSpeed)
        
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
    

#MAIN
timestep = 64
maxSpeed = -10

heading = 0
gpsLocation = ()
    
input = robot.getKeyboard()
input.enable(100)    
initilize_motors()

gps = robot.getGPS('gps')
gps.enable(500)

compass = robot.getCompass('compass')
compass.enable(100)

while robot.step(timestep) != -1:

    key = input.getKey()
    stop_moving()

    if(key > -1):
        read_keyboard_input(key,maxSpeed)
        
        
    tempLocation = gps.getValues() 
    gpsLocation = (tempLocation[0], tempLocation[1])
    gpsDestination = (4.362748731840904e-05, 4.257179007672356e-05)
    headingVector = compass.getValues()
    headingDegrees = math.degrees(math.atan2(headingVector[2],headingVector[0]))
    
    headingDegrees = abs((headingDegrees-360)%360)
    
    targetHeading = calculate_initial_compass_bearing(gpsLocation, gpsDestination)
    print(gpsLocation, headingDegrees)
        


#Functions    

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

# Enter here exit cleanup code.
