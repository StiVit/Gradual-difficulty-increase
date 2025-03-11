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