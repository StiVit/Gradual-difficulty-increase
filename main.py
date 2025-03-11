from app.simulation.environment import Plane
from app.neat_training.evaluate import eval_genomes
from app.genetic_algorithm.train_deap import run_evolution
from app.utils.logger import get_logger
import neat

if __name__ == "__main__":
    main_logger = get_logger("main_logger")
    plane = Plane(100, 100, num_food=100)
    
    # Run NEAT to train movement
    config_path = "app/neat_training/neat_config.txt"
    neat_population = neat.Population(neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                                  neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path))
    winner = neat_population.run(eval_genomes, 50)
    neat.Checkpointer.save_checkpoint("neat_best_model", winner)

    # Run Genetic Algorithm to evolve traits
    best_traits = run_evolution()
    main_logger.info(f"Best traits: {best_traits}")
