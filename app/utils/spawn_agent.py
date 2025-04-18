from app.environment.agent import Agent
import random
import neat

def spawn_agent(i, n_agents, x_plane, y_plane, net = None):
    if net:
        config_path = "app/neat_training/neat_config.txt"
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
        net = neat.nn.FeedForwardNetwork.create(net, config)
    quarter = n_agents // 4
    match i:
        case _ if i < quarter:
            return Agent(10, random.randint(10, y_plane-10), net=net)
        case _ if i < 2 * quarter:
            return Agent(x_plane-10, random.randint(10, y_plane-10), net=net)
        case _ if i < 3 * quarter:
            return Agent(random.randint(10, x_plane-10), 10, net=net)
        case _:
            return Agent(random.randint(10, x_plane-10), y_plane-10, net=net)