import matplotlib.pyplot as plt

def show_agents(width, height, agents):

    cords = [(agent[0].x, agent[0].y) for agent in agents]

    x_coords = [x for x, _ in cords]
    y_coords = [y for _, y in cords]

    plt.scatter(x_coords, y_coords, c='blue', marker='o')
    plt.title('Agents\' position')
    plt.xlabel('Width')
    plt.ylabel('Height')
    plt.xlim(0, width)
    plt.ylim(0, height)
    plt.grid(False)
    plt.show()