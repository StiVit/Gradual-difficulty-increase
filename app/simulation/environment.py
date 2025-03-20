"""
Defines the 2D plane and food spawning
"""

import random

class Plane:
    def __init__(self, width, height, num_food):
        self.width = width
        self.height = height
        self.food = self.spawn_food(num_food)
    
    def spawn_food(self, num_food):
        return [(random.uniform(0, self.width), random.uniform(0, self.height)) for _ in range(num_food)]
    
    def show_food(self):
        import matplotlib.pyplot as plt

        x_coords = [x for x, _ in self.food]
        y_coords = [y for _, y in self.food]

        plt.scatter(x_coords, y_coords, c='green', marker='o')
        plt.title('Food on the Plane')
        plt.xlabel('Width')
        plt.ylabel('Height')
        plt.xlim(0, self.width)
        plt.ylim(0, self.height)
        plt.grid(False)
        plt.show()