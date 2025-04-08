import pygame
import random
import neat
from app.simulation.environment import Plane
from app.genetic_algorithm.train_deap import run_evolution
from app.utils.settings import settings
from app.utils.helpers import spawn_agent

best_traits = run_evolution()
        
def visualize_game(winner):
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    plane = Plane(settings.x_plane, settings.y_plane, settings.food_count)

    agents = [spawn_agent(i, settings.n_agents, settings.x_plane, settings.y_plane, winner) for i in range(settings.n_agents)]

    while True:
        screen.fill((255, 255, 255))
        for food in plane.food:
            pygame.drew.circle(screen, (0, 255, 0), (int(food[0]), int(food[1])), 5)
        for agent in agents:
            agent.decide_movement(plane)
            pygame.draw.circle(screen, (255, 0, 0), (int(agent.x), int(agent.y)), int(agent.size * 3))

        pygame.display.flip()
        clock.tick(30)