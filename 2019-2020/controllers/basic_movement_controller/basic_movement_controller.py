"""my controller description."""
from controller import Robot, Motor

MAX_SPEED = 10
#TIME_STEP = 64

# create Robot
robot = Robot()

# instantiate devices on Robot
wheelsL = [Motor("left front motor"), Motor("left back motor")]
wheelsR = [Motor("right front motor"), Motor("right back motor")]

# get timestep
TIME_STEP = int(robot.getBasicTimeStep())

# set target position to infinity (speed control)
wheelsL[0].setPosition(float('inf'))
wheelsL[1].setPosition(float('inf'))
wheelsR[0].setPosition(float('inf'))
wheelsR[1].setPosition(float('inf'))

# set up the motor speed percentage of max speed
rightSpeedPercent = 0.70
leftSpeedPercent = 0.30

# set up motor speeds
wheelsL[0].setVelocity(leftSpeedPercent * MAX_SPEED)
wheelsL[1].setVelocity(leftSpeedPercent * MAX_SPEED)
wheelsR[0].setVelocity(rightSpeedPercent * MAX_SPEED)
wheelsR[1].setVelocity(rightSpeedPercent * MAX_SPEED)

while (robot.step(TIME_STEP) != -1):
  # Read the sensors, like:

  # Process sensor data here

  # Enter here functions to send actuator commands, like:
  pass

# Enter here exit cleanup code