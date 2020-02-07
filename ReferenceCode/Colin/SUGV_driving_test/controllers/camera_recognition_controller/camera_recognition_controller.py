"""touch sensor controller for SUGV"""
from controller import Robot, Motor, Keyboard, GPS, Compass, Camera, TouchSensor, CameraRecognitionObject
import math, random

# Constants
MAX_SPEED = 10
# TIME_STEP = 64
INCREMENT = 0.1
TURN_COEFFICIENT = 2.0
DISTANCE_TOLERANCE = 0.00001
M_PI = math.pi
LEFT = 0
RIGHT = 1

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

#bumper = TouchSensor('touch sensor')
#bumper.enable(250)
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

# set left and right motor speed [rad/s]
def robot_set_speed(left, right):
    for i in range(0,2):
        motors[i + 0].setVelocity(left)
        motors[i + 2].setVelocity(right)

# read keyboard input
def check_keyboard():
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

    robot_set_speed(speeds[LEFT], speeds[RIGHT])

# main loop
while (robot.step(TIME_STEP) != -1):
    check_keyboard()
    if(camera.getRecognitionNumberOfObjects() > 0):
        recognized = camera.getRecognitionObjects()
        pos_on_imag = recognized[0].get_position_on_image()
        size_on_imag = recognized[0].get_size_on_image()
        print("Pos on Image: {0:d},{1:.7f}     Size on Image: {2:.7f},{3:.7f}" .format(pos_on_imag[0], pos_on_imag[1], size_on_imag[0], size_on_imag[1]), end="\r")
