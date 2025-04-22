import matplotlib.pyplot as plt

def show_game(plane, agents):

    x_food_coords = [x for x, _ in plane.food]
    y_food_coords = [y for _, y in plane.food]
    agents_cords = [(agent[0].x, agent[0].y) for agent in agents]
    x_agent_coords = [x for x, _ in agents_cords]
    y_agent_coords = [y for _, y in agents_cords]


    plt.scatter(x_agent_coords, y_agent_coords, c='blue', marker='o')
    plt.scatter(x_food_coords, y_food_coords, c='green', marker='x')
    plt.title('Game')
    plt.xlabel('Width')
    plt.ylabel('Height')
    plt.xlim(0, plane.width)
    plt.ylim(0, plane.height)
    plt.grid(False)
    plt.show()