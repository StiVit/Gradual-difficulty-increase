from deap import base, creator, tools, algorithms # type: ignore
from app.neat_training.run_neat import run_neat
from app.environment.environment import Plane
from app.environment.agent import Agent
from app.utils.settings import settings
from app.utils.spawn_agent import spawn_agent
import pickle
import random

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_speed", random.randint, 1, 5)  # Speed range
toolbox.register("attr_sense", random.randint, 30, 300) # Sense range
toolbox.register("individual", tools.initCycle, creator.Individual, 
                 (toolbox.attr_speed, toolbox.attr_sense), n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    plane = Plane(settings.x_plane, settings.y_plane, 100)
    speed, sense = individual
    best_model_path = "app/neat_training/winner.pkl"
    with open(best_model_path, "rb") as f:
        net = pickle.load(f)
    agent = spawn_agent(0, 1, settings.x_plane, settings.y_plane, net=net)
    while agent.energy > 0:
        agent.decide_movement(plane)
    # Simulate agent behavior using NEAT-trained movement
    # Compute fitness based on performance
    return (agent.energy // 100) * agent.eaten,

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=0.1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)

def run_evolution():
    pop = toolbox.population(n=50)
    algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=20, verbose=True)
    return tools.selBest(pop, k=1)[0]
