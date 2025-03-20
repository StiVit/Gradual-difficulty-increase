import math

class Agent:
    def __init__(self, x, y, speed = 1.0, size = 1.0, sense = 500.0, net = None):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.sense = sense
        self.energy = 100 # Initial energy
        self.net = net
        self.eaten = False

    def move(self, direction):
        dx, dy = math.cos(direction) * self.speed, math.sin(direction) * self.speed
        self.x += dx
        self.y += dy
        self.energy -= self.speed * self.size # More spped and size, more energy consumed

    def perceive_food(self, food_list):
        return [food for food in food_list if self.distance_to(food) <= self.sense]

    def distance_to(self, target):
        return math.sqrt((self.x - target[0]) ** 2 + (self.y - target[1]) ** 2)
    
    def decide_movement(self, plane):
        if self.net:
            food_list = plane.food
            closest_food = min(food_list, key=lambda food: agent.distance_to(food), default=None)
            if closest_food:
                inputs = [self.x, self.y, closest_food[0] if closest_food else (-1, -1), self.energy]
            output = self.net.activate(inputs)
            direction = output[0] * 2 * math.pi
            self.move(direction)