"""keyboard controller with Autonomy for SUGV"""
from controller import Robot, Motor, Keyboard, GPS, Compass
import math

# Constants
MAX_SPEED = -10
# TIME_STEP = 64
INCREMENT = 0.1
TURN_COEFFICIENT = 4.0
DISTANCE_TOLERANCE = 1.5
TARGET_POINTS_SIZE = 13
M_PI = math.pi
LEFT = 0
RIGHT = 1

# Globals
current_target_index = 0
targets = [[-4.209318, -9.147717], [0.946812, -9.404304]]
autopilot = True
old_autopilot = True
old_key = -1

# create Robot
robot = Robot()

# create keyboard
kb = robot.getKeyboard()
kb.enable(250)

# instantiate devices on Robot
motors = [Motor("motor LRear"), Motor("motor LFront"), Motor("motor RRear"), Motor("motor RFront")]
gps = GPS('gps')
gps.enable(250)
compass = Compass('compass')
compass.enable(250)

# get timestep
TIME_STEP = int(robot.getBasicTimeStep())

# set target position to infinity (speed control)
for i in range(0,4):
    motors[i].setPosition(float('inf'))

print("You can drive this robot:")
print("Select the 3D window and use cursor keys:")
print("Press 'A' to return to the autopilot mode")
print("Press 'P' to get the robot position")

def modulus_double(a, m):
    div_d = a / m
    r = a - div_d * m
    if (r < 0.0):
        r += m
    return r

# set left and right motor speed [rad/s]
def robot_set_speed(left, right):
    for i in range(0,2):
        motors[i + 0].setVelocity(left)
        motors[i + 2].setVelocity(right)

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
                print("position: {%f, %f}\n", pos3D[0], pos3D[2])
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
    return math.sqrt(v[0] * v[0] + v[1] * v[1])

# v = v/||v||
def normalize(v):
    n = norm(v)
    v[0] /= n
    v[1] /= n

# v = v1-v2
def minus(v, v1, v2):
    v[0] = v1[0] - v2[0]
    v[1] = v1[1] - v2[1]

# compute the angle between two vectors
# return value: [0, 2Pi]
def angle(v1, v2):
    return modulus_double(math.atan2(v2[1], v2[0]) - math.atan2(v1[1], v1[0]), 2.0 * M_PI)

# autopilot
# pass trough the predefined target positions
def run_autopilot():
    # global variable pull
    global current_target_index

    # prepare the speed array
    speeds = [0.0, 0.0]

    # read gps position and compass values
    pos3D = gps.getValues()
    north3D = compass.getValues()
    print(pos3D)

    # compute the 2D position of the robo and its orientation
    pos = [pos3D[0], pos3D[2]]
    north = [north3D[0], north3D[2]]
    front = [-1*north[0], north[1]]

    # compute the direction and the distance to the target
    direction = [0,0]
    minus(direction, targets[current_target_index], pos)
    distance = norm(direction)
    normalize(direction)

    # compute the target angle
    beta = angle(front, direction) - M_PI

    # a target position has been reached
    if (distance < DISTANCE_TOLERANCE):
        print("target %d reached\n", current_target_index + 1)
        current_target_index += 1
        current_target_index %= TARGET_POINTS_SIZE
    
    # move the robot to the next target
    else:
        speeds[LEFT] = MAX_SPEED - M_PI + TURN_COEFFICIENT * beta
        speeds[RIGHT] = MAX_SPEED - M_PI - TURN_COEFFICIENT * beta

    # set the motor speeds
    robot_set_speed(speeds[LEFT], speeds[RIGHT])

 # print user instructions

# main loop
while (robot.step(TIME_STEP) != -1):
    check_keyboard()
    if (autopilot):
        run_autopilot()