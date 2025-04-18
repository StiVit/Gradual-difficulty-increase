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
    if len(output) != 4 or any(not isinstance(value, (int, float)) for value in output):
        raise ValueError("Wrong output format")
    directions = ['l', 'u', 'r', 'd']
    max_index = output.index(max(output))
    return directions[max_index]