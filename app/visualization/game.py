import pygame
import random
from app.environment.environment import Plane
from app.genetic_algorithm.train_deap import run_evolution
from app.utils.settings import settings
from app.utils.spawn_agent import spawn_agent, spawn_agent_in_one_line
from app.utils.helpers import get_closest_edge
from app.environment.agent import Agent

# best_traits = run_evolution()
        
def visualize_game(winner, human_player = False, difficulty_increase = False):
    pygame.init()
    screen = pygame.display.set_mode((settings.x_plane, settings.x_plane))
    clock = pygame.time.Clock()

    # Initialize font for displaying text
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    plane = Plane(settings.x_plane, settings.y_plane, settings.food_count)

    # Can use spawn_agent to spawn in all 4 edges
    # Spawn AI agents in one line
    agents = [spawn_agent_in_one_line(i, settings.n_agents, settings.x_plane, settings.y_plane, winner) for i in range(settings.n_agents)]

    # Add a player-controlled agent
    if human_player:
        player_agent = Agent(random.randint(0, settings.x_plane), settings.y_plane-10)
    else:
        player_agent = None

    while any(agent.energy > 0 for agent in agents) or (player_agent and player_agent.energy > 0):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill((255, 255, 255))

        # Draw the food sources
        for food in plane.food:
            pygame.draw.circle(screen, (0, 255, 0), (int(food[0]), int(food[1])), 5)


        # Update and draw AI agents
        for agent in agents:
            agent.decide_movement(plane)
            pygame.draw.circle(screen, (0, 0, 255), (int(agent.x), int(agent.y)), int(agent.size * 5))

            closest_food = sorted(agent.perceive_food(plane.food), key=lambda x: agent.distance_to(x))
            if closest_food:
                closest_food = closest_food[0]
            else:
                closest_food = None
            if closest_food and agent.distance_to(closest_food) <= agent.size+2:
                agent.eat()
                plane.food.remove(closest_food)


        if human_player:
            # Draw the player agent
            pygame.draw.circle(screen, (255, 0, 0), (player_agent.x, player_agent.y), player_agent.size *5)

            # Handle player movement with WASD keys
            keys = pygame.key.get_pressed()
            if player_agent.energy > 0:
                if keys[pygame.K_w]:
                    player_agent.move('d')
                if keys[pygame.K_a]:
                    player_agent.move('l')
                if keys[pygame.K_s]:
                    player_agent.move('u')
                if keys[pygame.K_d]:
                    player_agent.move('r')
        
            # player_agent_eat
            closest_food = sorted(player_agent.perceive_food(plane.food), key=lambda x: player_agent.distance_to(x))
            if closest_food:
                closest_food = closest_food[0]
            else:
                closest_food = None
            if closest_food and player_agent.distance_to(closest_food) <= player_agent.size + 2:
                player_agent.eat()
                plane.food.remove(closest_food)

            energy_text = font.render(f"Energy: {player_agent.energy}", True, (0, 0, 0))
            screen.blit(energy_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)
    
    if human_player and player_agent:
        fitness = 0
        if player_agent.distance_to(get_closest_edge(player_agent, settings.x_plane, settings.y_plane)) < 15:
            fitness = player_agent.energy // 10 + player_agent.eaten * 100

        if difficulty_increase:
            fitness += 50
        with open("player_fitness.txt", "w") as file:
            file.write(f"{fitness}")