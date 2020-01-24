"""basic keyboard controller for SUGV"""
from controller import Robot, Motor, Keyboard

MAX_SPEED = -10
# TIME_STEP = 64
INCREMENT = 0.1

# create Robot
robot = Robot()

# create keyboard
kb = robot.getKeyboard()
kb.enable(250)

# instantiate devices on Robot
wheelsL = [Motor("motor LRear"), Motor("motor LFront")]
wheelsR = [Motor("motor RRear"), Motor("motor RFront")]

# get timestep
TIME_STEP = int(robot.getBasicTimeStep())

# set target position to infinity (speed control)
wheelsL[0].setPosition(float('inf'))
wheelsL[1].setPosition(float('inf'))
wheelsR[0].setPosition(float('inf'))
wheelsR[1].setPosition(float('inf'))

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
    leftSpeed += INCREMENT
    rightSpeed += INCREMENT

    if(leftSpeed >= MAX_SPEED):
      leftSpeed = MAX_SPEED
    if(rightSpeed >= MAX_SPEED):
      rightSpeed = MAX_SPEED

    # print("w:%f:%f" %(leftSpeed, rightSpeed))

  # reverse
  if(key == ord('S')):
    leftSpeed -= INCREMENT
    rightSpeed -= INCREMENT

    if(leftSpeed <= -1*MAX_SPEED):
      leftSpeed = -1*MAX_SPEED
    if(rightSpeed <= -1*MAX_SPEED):
      rightSpeed = -1*MAX_SPEED

    # print("s:%f:%f" %(leftSpeed, rightSpeed))

  # turn left
  if(key == ord('A')):
    leftSpeed -= 2*INCREMENT
    rightSpeed += INCREMENT

    if(leftSpeed <= -1*MAX_SPEED):
      leftSpeed = -1*MAX_SPEED
    if(rightSpeed >= MAX_SPEED):
      rightSpeed = MAX_SPEED

    # print("a:%f:%f" %(leftSpeed, rightSpeed))

  # turn right
  if(key == ord('D')):
    leftSpeed += INCREMENT
    rightSpeed -= 2*INCREMENT

    if(leftSpeed >= MAX_SPEED):
      leftSpeed = MAX_SPEED
    if(rightSpeed <= -1*MAX_SPEED):
      rightSpeed = -1*MAX_SPEED

    # print("d:%f:%f" %(leftSpeed, rightSpeed))

  # no input
  if(key == -1):
    if(leftSpeed != 0):
      if(leftSpeed < 0):
        leftSpeed += 3*INCREMENT
      if(rightSpeed > 0):
        leftSpeed -= 3*INCREMENT
    else:
      leftSpeed = 0

    if(rightSpeed != 0):
      if(rightSpeed < 0):
        rightSpeed += 3*INCREMENT
      if(rightSpeed > 0):
        rightSpeed -= 3*INCREMENT
    else:
      rightSpeed = 0

    # print(" :%f:%f" %(leftSpeed, rightSpeed))

# set speed
  wheelsL[0].setVelocity(leftSpeed)
  wheelsL[1].setVelocity(leftSpeed)
  wheelsR[0].setVelocity(rightSpeed)
  wheelsR[1].setVelocity(rightSpeed)

  pass