import pygame
import random
import neat
from app.simulation.environment import Plane
from app.simulation.agent import Agent
from app.genetic_algorithm.train_deap import run_evolution

pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

plane = Plane(100, 100, 100)
best_traits = run_evolution()

def load_neat(config_path):
    return neat.Checkpointer.restore_checkpoint("neat-best_model")

neat_model = load_neat("app/neat_training/neat_config.txt")
agents = [Agent(0, random.randint(0, 50), *best_traits, net=neat_model) for _ in range(20)]

while True:
    screen.fill((255, 255, 255))
    for food in plane.food:
        pygame.drew.circle(screen, (0, 255, 0), (int(food[0]), int(food[1])), 5)
    for agent in agents:
        agent.decide_movement(plane)
        pygame.draw.circle(screen, (255, 0, 0), (int(agent.x), int(agent.y)), int(agent.size * 3))

    pygame.display.flip()
    clock.tick(30)