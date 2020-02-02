"""touch sensor controller for SUGV"""
from controller import Robot, Motor, Keyboard, GPS, Compass, TouchSensor
import math, random

# Constants
MAX_SPEED = 10
# TIME_STEP = 64

# Globals


# create Robot
robot = Robot()

# create keyboard
kb = robot.getKeyboard
kb.enable(250)

# instantiate devices on Robot
motors = [Motor("Motor_LB"), Motor("Motor_LF"), Motor("Motor_RB"), Motor("Motor_RF")]
gps = GPS('gps')
gps.enable(250)
compass = Compass('compass')
compass.enable(250)
bumper = TouchSensor('touch sensor')
bumper.enable(250)

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
    if (bumper.getValue() == True):
        print("Touch Detected!")