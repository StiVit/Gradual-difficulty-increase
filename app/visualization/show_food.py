import matplotlib.pyplot as plt

def show_food(plane):

    x_coords = [x for x, _ in plane.food]
    y_coords = [y for _, y in plane.food]

    plt.scatter(x_coords, y_coords, c='green', marker='o')
    plt.title('Food on the Plane')
    plt.xlabel('Width')
    plt.ylabel('Height')
    plt.xlim(0, plane.width)
    plt.ylim(0, plane.height)
    plt.grid(False)
    plt.show()