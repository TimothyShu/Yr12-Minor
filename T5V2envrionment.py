import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
from tf_agents.environments import py_environment
from tf_agents.specs import array_spec
from tf_agents.trajectories import time_step as ts
import T5V1
from tf_agents.environments import tf_py_environment

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
            shape=(11,), dtype=np.int32, minimum=0, maximum=20, name='observation')

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
        return ts.restart(np.zeros(11,).astype(np.int32))

    def _get_obs(self, curr_cabin: T5V1.Cabin) -> np.int32:
        observ = [group.Count_unalocated() for group in self._groups]
        #Add the remaining capacity of the current cabin
        if curr_cabin == None:
            observ.append(0)
        else:
            observ.append(curr_cabin.get_remaining_capacity())
        observation = np.array(observ, dtype=np.int32)
        return observation

    def _step(self, action):
        # Take an action and return a new time step
        if self._episode_ended:
            # The last episode ended, start a new episode
            return self.reset()

        # Select a group from 1 to len(groups)
        Curr_group = self._groups[action]
        
        #Find the current Cabin
        curr_cabin = None
        for cabin in self._cabins:
            if cabin.get_remaining_capacity() == 0:
                continue
            else:
                curr_cabin = cabin
                break
        else:
            #If all cabins are filled, then it is ended

            self._episode_ended = True
            #Check the number of splits
            splits = T5V1.count_splits(self._groups)
            reward = -splits + 10
            observation = self._get_obs(curr_cabin=curr_cabin)
            return ts.transition(observation, reward=reward, discount=1)
        
        #If they picked a group that is already empty, then exit with reward -1
        if Curr_group.Count_unalocated() == 0:
            reward = -1
            observation = self._get_obs(curr_cabin=curr_cabin)
            return ts.transition(observation, reward=reward, discount=1)

        #Allocate the group to the current Cabin
        curr_cabin.Add_Group(Curr_group)


        # Return the new time step
        # Remaining group size/capacity
        observation = self._get_obs(curr_cabin=curr_cabin)
        return ts.transition(observation, reward=0, discount=1.0)

if __name__ == "__main__":
    env = CabinEnvironment()
    train_env = tf_py_environment.TFPyEnvironment(env)
    print(train_env.action_spec())
    print(train_env.observation_spec())
    print(train_env.time_step_spec())
    print(train_env._current_time_step())