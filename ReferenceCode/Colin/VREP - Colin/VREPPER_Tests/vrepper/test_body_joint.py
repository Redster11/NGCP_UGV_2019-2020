import os,math,time
from vrepper import core
# sorry but that's how the namespace works

venv = core.vrepper(headless=False)
venv.start()

# load scene
current_dir = os.path.dirname(os.path.realpath(__file__))
venv.load_scene(current_dir + '/scenes/body_joint_wheel.ttt')

body = venv.get_object_by_name('body')
wheel = venv.get_object_by_name('wheel')
joint = venv.get_object_by_name('joint')

print(body.handle,wheel.handle,joint.handle)

simulation_time = 5

venv.start_blocking_simulation()

for i in range(simulation_time * 20):
    print('simulation step', i)
    print('body position', body.get_position())
    print('wheel orientation', wheel.get_orientation())

    joint.set_velocity(10 * math.sin(i/5))
    # you should see things moving back and forth

    venv.step_blocking_simulation() # forward 1 timestep

# stop the simulation and reset the scene:
venv.stop_blocking_simulation()

print('simulation ended. leaving in 5 seconds...')
time.sleep(5)
