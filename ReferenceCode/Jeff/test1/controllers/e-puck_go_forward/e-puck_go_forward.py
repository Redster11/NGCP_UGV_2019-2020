"""e-puck_go_forward controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor

TIME_STEP = 64

MAX_SPEED = 6.28

robot = Robot()

leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')

leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

leftMotor.setVelocity(MAX_SPEED)
rightMotor.setVelocity(MAX_SPEED)

while robot.step(TIME_STEP) != -1:
    pass
