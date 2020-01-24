from controller import Robot, Motor, DistanceSensor, Camera, Keyboard, GPS, Compass
import math

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = 64
maxSpeed = 6.28
leftSpeed = 0
rightSpeed = 0
heading = 0
    
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)
input = robot.getKeyboard()
input.enable(100)

gps = robot.getGPS('gps')
gps.enable(500)

camera = robot.getCamera('camera')
camera.enable(100)

compass = robot.getCompass('compass')
compass.enable(100)

while robot.step(timestep) != -1:


    key = input.getKey()
    print(key)
    if key == 87:
        rightSpeed = maxSpeed
        leftSpeed = maxSpeed
    elif key == 68:
        rightSpeed = -maxSpeed
        leftSpeed = maxSpeed
    elif key == 83:
        rightSpeed = -maxSpeed
        leftSpeed = -maxSpeed
    elif key == 65:
        rightSpeed = maxSpeed
        leftSpeed = -maxSpeed
    else:
        rightSpeed = 0
        leftSpeed = 0   
    
    rightMotor.setVelocity(rightSpeed)
    leftMotor.setVelocity(leftSpeed)
    
    headingVector = compass.getValues()
    headingDegrees = math.degrees(math.atan2(headingVector[2],headingVector[0]))
    
    #print(headingDegrees)
    print(gps.getValues())

#Functions    
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
