"""e-puck_go_forward controller."""

from controller import Robot, Motor, Camera

TIME_STEP = 64

MAX_SPEED = 6.28

# create the Robot instance.
robot = Robot()

# create and pull motors from robot
leftMotor = Motor('left wheel motor')
rightMotor = Motor('right wheel motor')

# set target position to infinity (speed control)
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

# set up the motor speed percentage of max speed
rightSpeedPercent = 0.70
leftSpeedPercent = 0.30

# set up motor speeds
leftMotor.setVelocity(leftSpeedPercent * MAX_SPEED)
rightMotor.setVelocity(rightSpeedPercent * MAX_SPEED)

while robot.step(TIME_STEP) != -1:
   pass
