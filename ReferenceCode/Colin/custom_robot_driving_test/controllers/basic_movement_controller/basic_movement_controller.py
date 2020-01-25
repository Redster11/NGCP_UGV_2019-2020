"""basic movement controller for SUGV"""
from controller import Robot, Motor, Keyboard

MAX_SPEED = 10
# TIME_STEP = 64
INCREMENT = 0.1

# create Robot
robot = Robot()

# create keyboard
kb = robot.getKeyboard()
kb.enable(250)

# instantiate devices on Robot
wheels = [Motor('wheel BL'), Motor('wheel BR'), Motor('wheel FL'), Motor('wheel FR')]

# get timestep
TIME_STEP = int(robot.getBasicTimeStep())

# wheel motor setup
wheels[0].setPosition(float('inf'))
wheels[1].setPosition(float('inf'))
wheels[2].setPosition(float('inf'))
wheels[3].setPosition(float('inf'))

key = None
leftSpeed = 0
rightSpeed = 0
while (robot.step(TIME_STEP) != -1):
  # poll keyboard key
  key = kb.getKey()
  # print(key)

  # DRIVING LOGIC
  # forward
  if(key == ord('W')):
    leftSpeed = MAX_SPEED
    rightSpeed = MAX_SPEED

  # reverse
  if(key == ord('S')):
    leftSpeed = -1*MAX_SPEED
    rightSpeed = -1*MAX_SPEED

  # turn left
  if(key == ord('A')):
    leftSpeed = -1*MAX_SPEED
    rightSpeed = MAX_SPEED

  # turn right
  if(key == ord('D')):
    leftSpeed = MAX_SPEED
    rightSpeed = -1*MAX_SPEED

  # no input
  if(key == -1):
    leftSpeed = 0
    rightSpeed = 0

# set speed
  wheels[0].setVelocity(leftSpeed)
  wheels[1].setVelocity(rightSpeed)
  wheels[2].setVelocity(leftSpeed)
  wheels[3].setVelocity(rightSpeed)

  pass