"""Main Controller for SUGV"""
from controller import Robot, Motor, Keyboard, GPS, Compass, Camera, CameraRecognitionObject, TouchSensor
import math, random

# Constants
MAX_SPEED = 60
# TIME_STEP = 64
INCREMENT = 0.1
TURN_COEFFICIENT = 4.0
DISTANCE_TOLERANCE = 0.00001
M_PI = math.pi
LEFT = 0
RIGHT = 1

# Globals
state = 1
current_target_index = 0
targets = [[33.9322583, -117.6311557], [33.9323662, -117.6308731]]
# targets = [[33.9322583, -117.6311557], [33.9323678, -117.6310562]]
autopilot = False
old_autopilot = False
old_key = -1
PIXEL_THRESHOLD = 10
counter = 0

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

bumper = TouchSensor('touch sensor')
bumper.enable(250)

camera = Camera('camera')
camera.enable(250)
camera.recognitionEnable(100)

# get timestep
TIME_STEP = int(robot.getBasicTimeStep())

# set target position to infinity (speed control)
for i in range(0,4):
    motors[i].setPosition(float('inf'))

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
def autonomous_nav():
    # global variable pull
    global current_target_index
    global targets
    global state

    # prepare the speed array
    speeds = [0.0, 0.0]

    # read gps position and compass values
    pos3D = gps.getValues()
    north3D = compass.getValues()
    # print(pos3D)

    # compute the 2D position of the robot and its orientation
    pos = [pos3D[0], pos3D[1]]
    north = [north3D[0], north3D[2]]
    front = [north[0], -1*north[1]]

    # generate random waypoint
    # targets.append([random.uniform(33.9314620, 33.9325890), random.uniform(-117.6312430, -117.6330461)])

    # compute the direction and the distance to the target
    direction = minus(targets[current_target_index], pos)
    distance = norm(direction)
    direction = normalize(direction)
    # print("Distance: {0:.7f}    Direction: {1:.7f}, {2:.7f}".format(distance, direction[0], direction[1]), end="\r")
    # print("Current Pos: {0:.7f},{1:.7f}     Target Pos: {2:.7f},{3:.7f}" .format(pos[0], pos[1], targets[current_target_index][0],targets[current_target_index][1]), end="\r")

    # compute the target angle
    beta = angle(front, direction) - M_PI/2
    # print("Front: {0:.7f}, {1:.7f}   Direction: {2:.7f}, {3:.7f}    Beta: {4:.7f}".format(front[0], front[1], direction[0], direction[1], beta), end="\r")

    # a target position has been reached
    if (distance < DISTANCE_TOLERANCE):
        print("\ntarget {0} reached" .format(current_target_index + 1))
        current_target_index += 1
        
        # Transition to next state
        if(current_target_index == 2):
            state = 2
            current_target_index = 0
    
    # move the robot to the next target
    else:
        speeds[LEFT] = MAX_SPEED - M_PI + TURN_COEFFICIENT * beta
        speeds[RIGHT] = MAX_SPEED - M_PI - TURN_COEFFICIENT * beta

    # set the motor speeds
    robot_set_speed(speeds[LEFT], speeds[RIGHT])

# Center object on frame
def centerOnFrame():
    # Globals
    global PIXEL_THRESHOLD
    global state
    global MAX_SPEED

    objectFound = camera.getRecognitionNumberOfObjects()
    left = 0
    right = 0

    if(objectFound > 0):    # Object found on frame, center
        recognized = camera.getRecognitionObjects()
        [PosX, PosY] = recognized[0].get_position_on_image()
        [SizeX, SizeY] = recognized[0].get_size_on_image()

        # print("Pos on Image: {0:.0f},{1:.0f}     Size on Image: {2:.0f},{3:.0f}" .format(PosX, PosY, SizeX, SizeY), end="\r")

        center_current = PosX
        center_goal = camera.getWidth() / 2
        center_diff = center_current - center_goal
        normalized_center_diff = abs(center_diff / camera.getWidth())

        # print("Current Center: {0:.0f}     True Center: {1:.0f}     Center Diff: {2:.0f}" .format(center_current, center_goal, center_diff), end="\r")
        
        if(center_diff > PIXEL_THRESHOLD):    # Need to rotate Right
            left = MAX_SPEED * normalized_center_diff
            right = -1 * MAX_SPEED * normalized_center_diff
        elif(center_diff < -1 * PIXEL_THRESHOLD):  # Need to rotate Left
            left = -1 * MAX_SPEED * normalized_center_diff
            right = MAX_SPEED * normalized_center_diff
        else:
            state = 3

    else:   # Object not found, look until it is found
        left = -1 * MAX_SPEED/4
        right = MAX_SPEED/4

    robot_set_speed(left, right)

# Drive forward until touch
def touchStop():
    # Globals
    global MAX_SPEED
    global state

    # Variables
    left = MAX_SPEED/4
    right = MAX_SPEED/4

    if (bumper.getValue() == 1.0):
        left = 0
        right = 0
        state = 4
    
    robot_set_speed(left, right)

# Generate delay amount for x seconds
def waitCount(seconds):
    # Globals
    global TIME_STEP

    return round(seconds * (1000/TIME_STEP))

# Wait in Transport for x seconds
def waitInTransport(seconds):
    # Globals
    global state
    global counter

    # Variables
    limit = waitCount(seconds)

    counter += 1

    if(counter == limit):
        counter = 0
        state = 5

# Unload from BUGV
def unload():
    # Globals
    global state
    global counter

    limit = waitCount(20)
    left = -1 * MAX_SPEED/4
    right = -1 * MAX_SPEED/4

    counter += 1

    if(counter == limit):
        counter = 0
        state = 6
        left = 0
        right = 0
    
    robot_set_speed(left,right)

# print user instructions
print("You can drive this robot:")
print("Select the 3D window and use arrow keys:")
print("Press 'A' to return to the autopilot mode")
print("Press 'P' to get the robot position")

# main loop
while (robot.step(TIME_STEP) != -1):
    check_keyboard()
    if (autopilot):
        if(state == 1):
            autonomous_nav()
        elif(state == 2):
            # recognitionToggle()
            centerOnFrame()
        elif(state == 3):
            touchStop()
        elif(state == 4):
            waitInTransport(10)
        elif(state == 5):
            unload()
        elif(state == 6):
            autonomous_nav()

    print("State: {0:d}" .format(state), end="\r")