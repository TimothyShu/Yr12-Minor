import tensorflow as tf
import numpy as np
from tf_agents.environments import tf_py_environment
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.utils import common

# Import the CabinEnvironment and create_agent functions
from T5V2envrionment import CabinEnvironment
from T5V2AIModel import create_agent

# Set up the training hyperparameters
num_iterations = 20000
initial_collect_steps = 1000
collect_steps_per_iteration = 1
replay_buffer_capacity = 10000
batch_size = 64
learning_rate = 1e-3
log_interval = 200

# Create the environment
train_py_env = CabinEnvironment()
eval_py_env = CabinEnvironment()
train_env = tf_py_environment.TFPyEnvironment(train_py_env)
eval_env = tf_py_environment.TFPyEnvironment(eval_py_env)

# Create the agent
time_step_spec = train_env.time_step_spec()
action_spec = train_env.action_spec()

agent = create_agent(time_step_spec, action_spec)
agent.initialize()

# Set up the replay buffer
replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec=agent.collect_data_spec,
    batch_size=train_env.batch_size,
    max_length=replay_buffer_capacity)

# Set up the data collection
def collect_step(environment, policy):
    time_step = environment.current_time_step()
    action_step = policy.action(time_step)
    next_time_step = environment.step(action_step.action)
    traj = trajectory.from_transition(time_step, action_step, next_time_step)

    # Add the trajectory to the replay buffer
    replay_buffer.add_batch(traj)

def collect_data(env, policy, buffer, steps):
    for _ in range(steps):
        collect_step(env, policy)

# Create the dataset for training the agent
dataset = replay_buffer.as_dataset(
    num_parallel_calls=3,
    sample_batch_size=batch_size,
    num_steps=2).prefetch(3)

# Set up the training
iterator = iter(dataset)
optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate)

# Define the metrics
"""train_metrics = [    
    tf.metrics.mean(tf.compat.v1.losses.mean_squared_error(labels, predictions))    
    for labels, predictions in agent.
    ]"""


# Define the training loop
def train_agent(num_iterations, eval_interval, iterator):
    for i in range(num_iterations):
        # Collect data
        collect_data(train_env, agent.policy, replay_buffer, collect_steps_per_iteration)

        # Sample a batch of data from the buffer
        try:
            experience, unused_info = next(iterator)
        except tf.errors.OutOfRangeError:
            iterator = iter(dataset)
            experience, unused_info = next(iterator)

        # Train the agent
        train_loss = common.function(agent.train)(experience)
        """for metric in train_metrics:
            metric(experience.reward, agent.q_network(experience.observation, experience.action))"""

        # Evaluate the agent
        if i % eval_interval == 0:
            avg_return = compute_avg_return(eval_env, agent.policy, num_episodes=10)
            print('Iteration {}: loss = {}, average return = {}'.format(i, train_loss, avg_return))



# Define a function to evaluate the agent
def compute_avg_return(environment, policy, num_episodes=10):
    total_return = 0.0
    for _ in range(num_episodes):
        time_step = environment.reset()
        episode_return = 0.0
        while not time_step.is_last():
            action_step = policy.action(time_step)
            time_step = environment.step(action_step.action)
            episode_return += time_step.reward
        total_return += episode_return
    avg_return = total_return / num_episodes
    return avg_return.numpy()[0]

train_agent(num_iterations=num_iterations, eval_interval=100, iterator=iterator)

compute_avg_return(environment=eval_env, policy=agent.policy, num_episodes=10)