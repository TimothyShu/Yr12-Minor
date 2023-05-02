import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts
import T5V1

class CabinEnvironment(py_environment.PyEnvironment):
    def __init__(self):

        #Create the env variables
        variables = T5V1.Create_env()
        students = variables[0]
        groups = variables[1]
        cabins = variables[2]

        # Define the action and observation specs

        #The AI has a list of groups, it will fill up cabins consequtively with groups they choose sequentially
        self._action_spec = array_spec.BoundedArraySpec(
            shape=(), dtype=np.int32, minimum=0, maximum=len(groups) - 1, name='action')
        #This action decides which group will be added next

        #This defines what the AI would be able to see.
        #Should be able to see (what is left of) all group sizes, current cabin free space
        # e.g. [[group0size, group1size, group2size ..., freespace]
        self._observation_spec = array_spec.BoundedArraySpec(
            shape=(len(groups)+1,), dtype=np.int32, minimum=0, maximum=20, name='observation')

        # Define any other necessary variables
        self._studentts = students
        self._groups = groups
        self._cabins = cabins
        self._num_splits = 0
        self._num_groups = len(groups)
        self._episode_ended = False

    def action_spec(self):
        return self._action_spec

    def observation_spec(self):
        return self._observation_spec

    def _reset(self):
        variables = T5V1.Create_env()
        students = variables[0]
        groups = variables[1]
        cabins = variables[2]
        # Reset the environment to its initial state
        self._studentts = students
        self._groups = groups
        self._cabins = cabins
        self._num_splits = 0
        self._episode_ended = False
        return ts.restart(np.array([0] * self._num_groups, dtype=np.int32))

    def _step(self, action):
        # Take an action and return a new time step
        if self._episode_ended:
            # The last episode ended, start a new episode
            return self.reset()

        # Update the cabins based on the action
        group_size = self._groups[action]
        for i in range(len(self._cabins)):
            if len(self._cabins[i]) + group_size <= 20:
                self._cabins[i].extend([action] * group_size)
                break

        # Check if the episode has ended
        if all(len(cabin) == 20 for cabin in self._cabins):
            self._episode_ended = True
            reward = 1.0
        else:
            reward = 0.0

        # Return the new time step
        observation = np.array([len(cabin) for cabin in self._cabins], dtype=np.int32)
        return ts.transition(observation, reward=reward, discount=1.0)
