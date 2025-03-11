"""
Input: Agent Position, closest food position, remaining energy
Output: Movement direction
"""

import neat
import random
import math
from app.simulation.agent import Agent
from app.simulation.environment import Plane

def eval_genomes(genomes, config):
    plane = Plane(100, 100, 100)
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        agent = Agent(x=0, y=random.uniform(0, 100))
        fitness = 0

        while agent.energy > 0:
            food_list = plane.food
            closest_food = min(food_list, key=lambda food: agent.distance_to(food), default=None)
            if closest_food:
                inputs = [agent.x, agent.y, closest_food[0], closest_food[1], agent.energy]
                output = net.activate(inputs)
                direction = output[0] * 2 * math.pi
                agent.move(direction)

                if agent.distance_to(closest_food) < agent.size:
                    plane.food.remove(closest_food)
            
            if agent.distance_to((0, agent.y)) < agent.size:
                fitness = agent.energy + len(plane.food) * 10
                break
        
        genome.fitness = fitness