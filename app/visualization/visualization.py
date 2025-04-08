import pygame
import random
import neat
from app.simulation.environment import Plane
from app.genetic_algorithm.train_deap import run_evolution
from app.utils.settings import settings
from app.utils.spawn_agent import spawn_agent

best_traits = run_evolution()
        
def visualize_game(winner):
    pygame.init()
    screen = pygame.display.set_mode((settings.x_plane, settings.x_plane))
    clock = pygame.time.Clock()

    plane = Plane(settings.x_plane, settings.y_plane, settings.food_count)

    agents = [spawn_agent(i, settings.n_agents, settings.x_plane, settings.y_plane, winner) for i in range(settings.n_agents)]

    while any(agent.energy > 0 for agent in agents):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((255, 255, 255))
        for agent in agents:
            agent.decide_movement(plane)
            pygame.draw.circle(screen, (0, 0, 255), (int(agent.x), int(agent.y)), int(agent.size * 5))

            closest_food = sorted(agent.perceive_food(plane.food), key=lambda x: agent.distance_to(x))
            if closest_food:
                closest_food = closest_food[0]
            else:
                closest_food = None
            if closest_food and agent.distance_to(closest_food) <= agent.size:
                agent.eat()
                plane.food.remove(closest_food)
        
        for food in plane.food:
            pygame.draw.circle(screen, (0, 255, 0), (int(food[0]), int(food[1])), 5)

        pygame.display.flip()
        clock.tick(30)