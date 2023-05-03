import tensorflow as tf
from tf_agents.agents.dqn import dqn_agent
from tf_agents.networks import q_network
from tf_agents.utils import common

def create_agent(time_step_spec, action_spec):
    # Define the Q network
    fc_layer_params = (100,)
    q_net = q_network.QNetwork(
        time_step_spec.observation,
        action_spec,
        fc_layer_params=fc_layer_params)

    # Define the DQN agent
    optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate=0.001)
    train_step_counter = tf.Variable(0)
    agent = dqn_agent.DqnAgent(
        time_step_spec,
        action_spec,
        q_network=q_net,
        optimizer=optimizer,
        td_errors_loss_fn=common.element_wise_squared_loss,
        train_step_counter=train_step_counter)

    # Set the agent's policies
    agent.initialize()

    return agent