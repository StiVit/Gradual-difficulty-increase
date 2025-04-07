"""
Input: Agent Position, closest food position, remaining energy, distance to the closest food
Output: Movement direction
"""

import neat
import random
from app.simulation.agent import Agent
from app.simulation.environment import Plane
from app.utils.logger import get_logger
from app.visualization.show_game import show_game
from app.visualization.show_agents import show_agents

evaluation_logger = get_logger("evaluation_logger")
gen = 0

def eval_genomes(genomes, config):
    global gen
    evaluation_logger.debug(f"Active Generation: {gen}")
    n_agents = len(genomes)
    x_plane, y_plane = 1000, 1000
    plane = Plane(x_plane, y_plane, 200)

    agents = []
    nets = []
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        agent = spawn_agent(genome_id%100, n_agents, x_plane, y_plane)
        genome.fitness = 0
        agents.append((agent, genome_id, genome))
        nets.append(net)

    # For the purpose of visualization of the agents on the grid
    # show_agents(x_plane, y_plane, agents)

    while any(agent.energy > 0 for agent, _, _ in agents):
        if gen == 1:
            show_game(plane, agents)

        for i, (agent, genome_id, genome) in enumerate(agents):
            fitness = 0
            if agent.energy <= 0:
                continue
            
            # Get the closest food (if any) and the closest edge
            food_list = plane.food
            closest_food = sorted(agent.perceive_food(food_list), key=lambda x: agent.distance_to(x))
            if closest_food:
                closest_food = closest_food[0]
            else:
                closest_food = (-1, -1)
            closest_edge = get_closest_edge(agent, x_plane, y_plane)

            # Set all the inputs for the neural network
            inputs = [int(agent.x / x_plane * 100), 
                      int(agent.y / y_plane * 100), 
                      int(closest_food[0] / x_plane * 100), 
                      int(closest_food[1] / y_plane * 100),
                      int(closest_edge[0] / x_plane * 100),
                      int(closest_edge[1] / y_plane * 100),
                      agent.eaten, 
                      int(agent.energy) / 1000 * 100]
            output = nets[i].activate(inputs)

            direction = get_direction(output)
            agent.move(direction, x_plane, y_plane)

            if agent.distance_to(closest_food) <= agent.size:
                agent.eat()
                plane.food.remove(closest_food)
                fitness += 10 # Reward for eating food

            if agent.distance_to(closest_edge)-5 <= agent.size and agent.energy > 0 and agent.eaten:
                fitness = agent.energy // 10 + agent.eaten * 100
                evaluation_logger.info(f"Agent {genome_id}: E = {agent.energy}, Food Eaten = {agent.eaten}")
                agent.energy = 0  # Mark agent as finished
            
            genome.fitness += fitness
    evaluation_logger.info(f"Food left: {len(plane.food)}")
    gen += 1
    

def spawn_agent(i, n_agents, x_plane, y_plane):
    quarter = n_agents // 4
    match i:
        case _ if i < quarter:
            return Agent(10, random.randint(10, y_plane-10))
        case _ if i < 2 * quarter:
            return Agent(x_plane-10, random.randint(10, y_plane-10))
        case _ if i < 3 * quarter:
            return Agent(random.randint(10, x_plane-10), 10)
        case _:
            return Agent(random.randint(10, x_plane-10), y_plane-10)
        

def get_closest_edge(agent, x_plane, y_plane):
    edges = [
        (0, agent.y),  # Left edge
        (x_plane, agent.y),  # Right edge
        (agent.x, 0),  # Bottom edge
        (agent.x, y_plane)  # Top edge
    ]
    closest_edge = min(edges, key=lambda edge: agent.distance_to(edge))
    return closest_edge


def get_direction(output):
    directions = ['l', 'u', 'r', 'd']
    max_index = output.index(max(output))
    return directions[max_index]