"""keyboard controller with Autonomy for SUGV"""
from controller import Robot, Motor, Keyboard, GPS, Compass, Camera, CameraRecognitionObject
import math, random

# Constants
MAX_SPEED = 60
# TIME_STEP = 64
INCREMENT = 0.1
TURN_COEFFICIENT = 2.0
DISTANCE_TOLERANCE = 0.00001
M_PI = math.pi
LEFT = 0
RIGHT = 1

# Globals
current_target_index = 0
# targets = [[0.00001, 0.00004], [0.00000, 0.00000], [-0.00000, -0.00004], [-0.0000, -0.00001]]
targets = [[33.9323671, -117.6309513]]
autopilot = False
old_autopilot = False
old_key = -1

# create Robot
robot = Robot()

# create keyboard
kb = robot.getKeyboard()
kb.enable(250)

# instantiate devices on Robot
motors = [Motor("Motor_LB"), Motor("Motor_LF"), Motor("Motor_RB"), Motor("Motor_RF")]

gps = GPS('gps')
gps.enable(250)

compass = Compass('compass')
compass.enable(250)

camera = Camera('camera')
camera.enable(250)
camera.recognitionEnable(100)

# get timestep
TIME_STEP = int(robot.getBasicTimeStep())

# set target position to infinity (speed control)
for i in range(0,4):
    motors[i].setPosition(float('inf'))

 # print user instructions
print("You can drive this robot:")
print("Select the 3D window and use arrow keys:")
print("Press 'A' to return to the autopilot mode")
print("Press 'P' to get the robot position")

# set left and right motor speed [rad/s]
def robot_set_speed(left, right):
    for i in range(0,2):
        motors[i + 0].setVelocity(left)
        motors[i + 2].setVelocity(right)

# read keyboard input
def check_keyboard():
    # global variable pull
    global old_key
    global old_autopilot
    global autopilot

    speeds = [0.0, 0.0]

    key = kb.getKey()
    if (key >= 0):
        if(key == kb.UP):
            speeds[LEFT] = MAX_SPEED
            speeds[RIGHT] = MAX_SPEED
            autopilot = False
        if(key == kb.DOWN):
            speeds[LEFT] = -MAX_SPEED
            speeds[RIGHT] = -MAX_SPEED
            autopilot = False
        if(key == kb.RIGHT):
            speeds[LEFT] = MAX_SPEED
            speeds[RIGHT] = -MAX_SPEED
            autopilot = False
        if(key == kb.LEFT):
            speeds[LEFT] = -MAX_SPEED
            speeds[RIGHT] = MAX_SPEED
            autopilot = False
        if(key == ord('P')):
            if (key != old_key):  # perform this action just once
                pos3D = gps.getValues()
                print("position: {0:.7f}, {1:.7f}" .format(pos3D[0], pos3D[1]))
        if(key == ord('A')):
            if (key != old_key):  # perform this action just once
                autopilot = not autopilot

    if (autopilot != old_autopilot):
        old_autopilot = autopilot
        if (autopilot):
            print("auto control\n")
        else:
            print("manual control\n")

    robot_set_speed(speeds[LEFT], speeds[RIGHT])
    old_key = key

# ||v||
def norm(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

# v = v/||v||
# return value: unit scale norm of vector [0:1][0:1]
def normalize(v):
    n = norm(v)
    v[0] /= n
    v[1] /= n
    return v

# subtract 'vectors'
# return value: v[] = v1[]-v2[] element-wise
def minus(v1, v2):
    v = [None,None]
    v[0] = v1[0] - v2[0]
    v[1] = v1[1] - v2[1]
    return v

# compute the angle between two vectors
# return value: [0, 2Pi]
def angle(v1, v2):
    dotProduct = v1[0]*v2[0] + v1[1]*v2[1]
    # for three dimensional simply add dotProduct = a*c + b*d  + e*f 

    magnitudeProduct = math.sqrt(v1[0]*v1[0] + v1[1]*v1[1]) * math.sqrt(v2[0]*v2[0] + v2[1]*v2[1]) 
    # for three dimensional simply add modOfVector = math.sqrt( a*a + b*b + e*e)*math.sqrt(c*c + d*d +f*f) 

    angle = dotProduct/magnitudeProduct
    theta = math.acos(angle)
    return theta

# autopilot to pass trough the predefined target positions
def run_autopilot():
    # global variable pull
    global current_target_index
    global targets

    # prepare the speed array
    speeds = [0.0, 0.0]

    # read gps position and compass values
    pos3D = gps.getValues()
    north3D = compass.getValues()
    # print(pos3D)

    # compute the 2D position of the robo and its orientation
    pos = [pos3D[0], pos3D[1]]
    north = [north3D[0], north3D[2]]
    front = [north[0], -1*north[1]]

    # generate random waypoint
    # targets.append([0.00000063*random.randrange(-100,100,1),0.00000063*random.randrange(-100,100,1)])
    targets.append([random.uniform(33.9314620, 33.9325890), random.uniform(-117.6312430, -117.6330461)])

    # compute the direction and the distance to the target
    direction = minus(targets[current_target_index], pos)
    distance = norm(direction)
    direction = normalize(direction)
    # print("Distance: {0:.7f}    Direction: {1:.7f}, {2:.7f}".format(distance, direction[0], direction[1]), end="\r")
    print("Current Pos: {0:.7f},{1:.7f}     Target Pos: {2:.7f},{3:.7f}" .format(pos[0], pos[1], targets[current_target_index][0],targets[current_target_index][1]), end="\r")

    # compute the target angle
    beta = angle(front, direction) - M_PI/2
    # print("Front: {0:.7f}, {1:.7f}   Direction: {2:.7f}, {3:.7f}    Beta: {4:.7f}".format(front[0], front[1], direction[0], direction[1], beta), end="\r")

    # a target position has been reached
    if (distance < DISTANCE_TOLERANCE):
        print("\ntarget {0} reached" .format(current_target_index + 1))
        current_target_index += 1
    
    # move the robot to the next target
    else:
        speeds[LEFT] = MAX_SPEED - M_PI + TURN_COEFFICIENT * beta
        speeds[RIGHT] = MAX_SPEED - M_PI - TURN_COEFFICIENT * beta

    # set the motor speeds
    robot_set_speed(speeds[LEFT], speeds[RIGHT])

# main loop
while (robot.step(TIME_STEP) != -1):
    check_keyboard()
    if (autopilot):
        run_autopilot()