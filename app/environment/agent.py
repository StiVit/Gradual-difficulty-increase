from app.utils.settings import settings
from app.utils.helpers import get_closest_edge, get_direction

class Agent:
    def __init__(self, x, y, speed = settings.default_speed, sense = settings.default_sense, net = None):
        self.x = x
        self.y = y
        self.speed = speed
        self.sense = sense
        self.size = 1
        self.energy = settings.default_energy # Initial energy
        self.net = net
        self.eaten = 0

    def move(self, direction):
        match direction:
            case 'l':
                self.x -= self.speed if self.x >= self.speed else 0
            case 'r':
                self.x += self.speed if self.x <= settings.x_plane - self.speed else 0
            case 'u':
                self.y += self.speed if self.y <= settings.y_plane - self.speed else 0
            case 'd':
                self.y -= self.speed if self.y >= self.speed else 0
            case _:
                raise ValueError("Invalid direction of movement")
        self.energy -= self.speed * max(1, self.sense // 100) # More speed and sense, more energy consumed

    def perceive_food(self, food_list):
        return [food for food in food_list if self.distance_to(food) <= self.sense]

    def distance_to(self, target):
        if int(target[0]) != target[0] or int(target[1]) != target[1]:
            raise ValueError("Invalid coordinates")
        return abs(self.x - target[0]) + abs(self.y - target[1])
    
    def eat(self):
        if self.energy > 0:
            self.eaten += 1
            self.energy += 10
    
    def decide_movement(self, plane):
        if not self.net:
            return

        if self.energy <= 0:
            return
        
        x_plane, y_plane = settings.x_plane, settings.y_plane
        food_list = plane.food
        closest_food = sorted(self.perceive_food(food_list), key=lambda x: self.distance_to(x))
        if closest_food:
            closest_food = closest_food[0]
        else:
            closest_food = (-1, -1)
        closest_edge = get_closest_edge(self, x_plane, y_plane)
        inputs = [int(self.x), 
                      int(self.y), 
                      int(closest_food[0]), 
                      int(closest_food[1]),
                      int(closest_edge[0]),
                      int(closest_edge[1]),
                      self.eaten, 
                      int(self.energy)]
        output = self.net.activate(inputs)
        direction = get_direction(output)
        self.move(direction)

        if self.distance_to(closest_edge)-5 <= self.size and self.energy > 0 and self.eaten:
            self.energy = 0
            print("Agent finished iteration")