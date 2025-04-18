"""
Input: Agent Position, closest food position, remaining energy, distance to the closest food
Output: Movement direction
"""

import neat
from app.environment.environment import Plane
from app.utils.logger import get_logger
from app.utils.settings import settings
from app.utils.helpers import get_closest_edge, get_direction
from app.utils.spawn_agent import spawn_agent

evaluation_logger = get_logger("evaluation_logger")
gen = 0

def eval_genomes(genomes, config):
    global gen
    evaluation_logger.debug(f"Active Generation: {gen}")
    n_agents = settings.n_agents
    x_plane, y_plane = settings.x_plane, settings.y_plane
    plane = Plane(x_plane, y_plane, settings.food_count)

    agents = []
    nets = []
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        agent = spawn_agent(genome_id%100, n_agents, x_plane, y_plane)
        genome.fitness = 0
        agents.append((agent, genome_id, genome))
        nets.append(net)

    while any(agent.energy > 0 for agent, _, _ in agents):
        # if gen == 25:
        #     show_game(plane, agents)

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
            inputs = [int(agent.x), 
                      int(agent.y), 
                      int(closest_food[0]), 
                      int(closest_food[1]),
                      int(closest_edge[0]),
                      int(closest_edge[1]),
                      agent.eaten, 
                      int(agent.energy)]
            output = nets[i].activate(inputs)

            direction = get_direction(output)
            agent.move(direction)

            if agent.distance_to(closest_food) <= agent.size:
                agent.eat()
                plane.food.remove(closest_food)
                fitness += 10 # Reward for eating food

            if agent.distance_to(closest_edge)-5 <= agent.size and agent.energy > 0 and agent.eaten:
                fitness = 100 + agent.energy // 10 + agent.eaten * 100
                evaluation_logger.info(f"Agent {genome_id}: E = {agent.energy}, Food Eaten = {agent.eaten}")
                agent.energy = 0  # Mark agent as finished
            
            genome.fitness += fitness
    evaluation_logger.info(f"Food left: {len(plane.food)}")
    gen += 1
    

