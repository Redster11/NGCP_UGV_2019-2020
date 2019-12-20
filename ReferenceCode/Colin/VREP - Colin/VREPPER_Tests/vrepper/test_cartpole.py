import vrepper
from vrepper.core import vrepper

import os,time
import numpy as np

import gym
from gym import spaces
#from gym.utils import colorize, seeding

class CartPoleVREPEnv(gym.Env):
    def __init__(self,headless=False):
        self.venv = venv = vrepper(headless=headless)
        venv.start()
        current_dir = os.path.dirname(os.path.realpath(__file__))
        venv.load_scene(current_dir + '/scenes/cart_pole.ttt')

        self.slider = venv.get_object_by_name('slider')
        self.cart = venv.get_object_by_name('cart')
        self.mass = venv.get_object_by_name('mass')

        print('(CartPoleVREP) initialized')

        obs = np.array([np.inf]*6)
        act = np.array([1.])

        self.action_space = spaces.Box(-act,act)
        self.observation_space = spaces.Box(-obs,obs)

    def _self_observe(self):
        # observe then assign
        cartpos = self.cart.get_position()
        masspos = self.mass.get_position()
        cartvel,cart_angvel = self.cart.get_velocity()
        massvel,mass_angvel = self.cart.get_velocity()

        self.observation = np.array([
            cartpos[0],cartvel[0],
            masspos[0],masspos[2],
            massvel[0],massvel[2]
            ]).astype('float32')

    def _step(self,actions):
        actions = np.clip(actions, -1, 1)
        v = actions[0]

        # step
        self.slider.set_velocity(v)
        self.venv.step_blocking_simulation()

        # observe again
        self._self_observe()

        # cost
        height_of_mass = self.observation[3] # masspos[2]
        cost = - height_of_mass + (v**2) * 0.001

        return self.observation, -cost, False, {}

    def _reset(self):
        self.venv.stop_blocking_simulation()
        self.venv.start_blocking_simulation()
        self._self_observe()
        return self.observation

    def _destroy(self):
        self.venv.stop_blocking_simulation()
        self.venv.end()

if __name__ == '__main__':
    env = CartPoleVREPEnv(headless=False)
    simulation_time = 15
    observation = env._reset()
    for j in range(simulation_time * 20):
        action = env.action_space.sample() # your agent here (this takes random actions)
        observation, reward, done, info = env._step(action)
        print(reward)

    print('simulation ended. leaving in 5 seconds...')
    time.sleep(5)
