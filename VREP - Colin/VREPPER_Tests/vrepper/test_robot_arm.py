### This demo is using the Poppy Ergo Jr. robotic arm.
### We've developed this arm at INRIA Bordeaux.
### It's a cheap open source arm, i.e. you can just make it yourself.
### We also sell the parts online in a pack for around 300$.

import os
import numpy as np
import time
import matplotlib.pyplot as plt

from vrepper.core import vrepper

venv = vrepper(headless=True)
venv.start()
current_dir = os.path.dirname(os.path.realpath(__file__))
venv.load_scene(current_dir + '/scenes/poppy_ergo_jr.ttt')
motors = []
for i in range(6):
    motor = venv.get_object_by_name('m{}'.format(i + 1), is_joint=True)
    motors.append(motor)

cam = venv.get_object_by_name("cam")

venv.start_simulation(is_sync=False)  # start in realtime mode to set initial position


def set_motors(positions, speeds=None):
    for i, m in enumerate(motors):
        target = positions[i]
        if i == 0:  # first joint is inverted in simulation
            target *= -1
        m.set_position_target(target)
        if speeds is not None:
            m.set_velocity(speeds[i])


def get_motors():
    out_pos = np.zeros(6, dtype=np.float32)
    out_vel = np.zeros(6, dtype=np.float32)
    for i, m in enumerate(motors):
        angle = m.get_joint_angle()
        if i == 0:  # first joint is inverted in simulation
            angle *= -1
        out_pos[i] = angle
        out_vel[i] = m.get_joint_velocity()[0]

    return out_pos, out_vel


# init position for this turn
inital_pose = [45, -90, 0, 0, 75, 0]
set_motors(inital_pose)
time.sleep(.2)  # go to inital pose, then disable realtime-mode
venv.make_simulation_synchronous(True)

# setup the viewer for the camera images
plt.ion()
img = np.random.uniform(0, 255, (256, 512, 3))
plt_img = plt.imshow(img, interpolation='none', animated=True, label="blah")
plt_ax = plt.gca()


def update_img():
    sim_img = venv.get_image(cam.handle)
    sim_depth = venv.get_depth_image_as_rgb(cam.handle)
    # in production you probably don't need the 3 channel depth image, but rather the 1 channel img
    # which you can get via venv.get_depth_image_as_image(cam.handle).
    # I'm only using it here so that I can show the two images side-by-side in a plot.

    img_tmp = np.zeros((256, 512, 3), dtype=np.uint8)
    # img_tmp[:, :256, :] = np.rot90(sim_img, 2, (0, 1))  # rotate image 180 degr
    # img_tmp[:, 256:, :] = np.rot90(sim_depth, 2, (0, 1))
    img_tmp[:, :256, :] = sim_img  # I don't understand ... sometimes the image is 180 turned, sometimes it isn't
    img_tmp[:, 256:, :] = sim_depth
    return img_tmp


for i in range(100):
    if i % 10 == 0:
        action = np.random.uniform(-90, 90, 6)
    set_motors(action)
    venv.step_blocking_simulation()

    motor_pos, motor_vel = get_motors()
    print (motor_pos, motor_vel)

    plt_img.set_data(update_img())
    plt_ax.plot([0])
    plt.pause(0.001)  # I found this necessary - otherwise no visible img
