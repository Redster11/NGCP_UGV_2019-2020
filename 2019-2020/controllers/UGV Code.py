"""my controller description."""
from controller import *

robot = Robot()

timestep = int(robot.getBasicTimeStep())

led = robot.getLED('ledName')
distanceSensor = robot.getDistanceSensor('distanceSensorName')
distanceSensor.enable(timestep)
wheelsR[] = {robot.getMotor("right front motor"), robot.getMotor("right back motor")}
print(wheelsR[0].getType())
while (robot.step(timestep) != -1):
  # Read the sensors, like:
  val = distanceSensor.getValue()

  # Process sensor data here

  # Enter here functions to send actuator commands, like:
  led.set(1)

# Enter here exit cleanup code