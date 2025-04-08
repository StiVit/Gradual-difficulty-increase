from app.simulation.agent import Agent
import random

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