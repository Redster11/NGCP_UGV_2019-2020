"""touch sensor controller for SUGV"""
from controller import Robot, Motor, Keyboard, GPS, Compass, Camera, TouchSensor, CameraRecognitionObject
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
PIXEL_THRESHOLD = 10
centerMode = False

# Globals

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

# print user instructions
print("You can drive this robot:")
print("Select the 3D window and use arrow keys:")
print("To center object on frame press 'C':")

# set left and right motor speed [rad/s]
def robot_set_speed(left, right):
    for i in range(0,2):
        motors[i + 0].setVelocity(left)
        motors[i + 2].setVelocity(right)

# read keyboard input
def check_keyboard():
    # Globals
    global old_key
    global centerMode

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
        if(key == ord('C')):
            if (key != old_key):  # perform this action just once
                centerMode = not centerMode

    robot_set_speed(speeds[LEFT], speeds[RIGHT])
    old_key = key

# center object on frame
def centerOnFrame():
    # Globals
    global PIXEL_THRESHOLD

    if(camera.getRecognitionNumberOfObjects() > 0):
        recognized = camera.getRecognitionObjects()
        [PosX, PosY] = recognized[0].get_position_on_image()
        [SizeX, SizeY] = recognized[0].get_size_on_image()

        # print("Pos on Image: {0:.0f},{1:.0f}     Size on Image: {2:.0f},{3:.0f}" .format(PosX, PosY, SizeX, SizeY), end="\r")

        center_current = PosX
        center_goal = camera.getWidth() / 2
        center_diff = center_current - center_goal
        normalized_center_diff = abs(center_diff / camera.getWidth())

        print("Current Center: {0:.0f}     True Center: {1:.0f}     Center Diff: {2:.0f}" .format(center_current, center_goal, center_diff), end="\r")
        
        if(center_diff > PIXEL_THRESHOLD):    # Need to rotate Right
            left = MAX_SPEED * normalized_center_diff
            right = -1 * MAX_SPEED * normalized_center_diff
        elif(center_diff < -1 * PIXEL_THRESHOLD):  # Need to rotate Left
            left = -1 * MAX_SPEED * normalized_center_diff
            right = MAX_SPEED * normalized_center_diff

        robot_set_speed(left, right)

# main loop
while (robot.step(TIME_STEP) != -1):
    check_keyboard()
    if(centerMode):
        centerOnFrame()