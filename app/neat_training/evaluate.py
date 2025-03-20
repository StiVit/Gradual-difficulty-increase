"""
Input: Agent Position, closest food position, remaining energy
Output: Movement direction
"""

import neat
import random
import math
from app.simulation.agent import Agent
from app.simulation.environment import Plane
from app.utils.logger import get_logger

evaluation_logger = get_logger("evaluation_logger")

def eval_genomes(genomes, config):
    plane_x, plane_y = 1000, 1000
    plane = Plane(plane_x, plane_y, 100)

    agents = []
    nets = []
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        agent = Agent(x=0, y=random.uniform(0, plane_y))
        genome.fitness = 0
        agents.append((agent, genome_id, genome))
        nets.append(net)

    while any(agent.energy > 0 for agent, _, _ in agents):
        for i, (agent, genome_id, genome) in enumerate(agents):
            if agent.energy <= 0:
                continue

            food_list = plane.food
            closest_food = sorted(agent.perceive_food(food_list), key=lambda x: agent.distance_to(x))
            if closest_food:
                closest_food = closest_food[0]
                # Do the preprocessing of the data to make the inputs fit together nicely
                inputs = [agent.x, agent.y, closest_food[0], closest_food[1], agent.energy, agent.distance_to(closest_food)]
                output = nets[i].activate(inputs)
                evaluation_logger.info(f"Agent: {genome_id}, Inputs: {inputs}, Output: {output}")

                direction = output[0] * 2 * math.pi
                agent.move(direction)

                if agent.distance_to(closest_food) <= agent.size:
                    agent.eaten = True
                    plane.food.remove(closest_food)
                    agent.energy += 50  # Reward for eating food

                if agent.distance_to((0, agent.y)) < agent.size and agent.energy > 0 and agent.eaten:
                    fitness = agent.energy + (100 - len(plane.food)) * 10
                    genome.fitness = fitness
                    evaluation_logger.info(f"Agent {genome_id}: {agent.energy}, {len(plane.food)}")
                    agent.energy = 0  # Mark agent as finished
            
            else:
                direction = random.uniform(0, 1) * 2 * math.pi
                agent.move(direction)