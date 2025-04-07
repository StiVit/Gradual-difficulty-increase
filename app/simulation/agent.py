import math

class Agent:
    def __init__(self, x, y, speed = 1.0, sense = 50.0, net = None):
        self.x = x
        self.y = y
        self.speed = speed
        self.sense = sense
        self.size = 1
        self.energy = 1000 # Initial energy
        self.net = net
        self.eaten = 0

    def move(self, direction, x_plane, y_plane):
        match direction:
            case 'l':
                self.x -= self.speed if self.x >= self.speed else 0
            case 'r':
                self.x += self.speed if self.x <= x_plane - self.speed else 0
            case 'u':
                self.y += self.speed if self.y <= y_plane - self.speed else 0
            case 'd':
                self.y -= self.speed if self.y >= self.speed else 0
        self.energy -= self.speed * max(1, self.sense // 100) # More speed and sensd, more energy consumed

    def perceive_food(self, food_list):
        return [food for food in food_list if self.distance_to(food) <= self.sense]

    def distance_to(self, target):
        return abs(self.x - target[0]) + abs(self.y - target[1])
    
    def eat(self):
        if self.energy > 0:
            self.eaten += 1
            self.energy += 10
    
    def decide_movement(self, plane):
        # Stand for modification
        if self.net:
            food_list = plane.food
            closest_food = min(food_list, key=lambda food: self.distance_to(food), default=None)
            if closest_food:
                inputs = [self.x, self.y, closest_food[0] if closest_food else (-1, -1), self.energy]
            output = self.net.activate(inputs)
            direction = output[0] * 2 * math.pi
            self.move(direction)