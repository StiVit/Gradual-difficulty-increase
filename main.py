from app.simulation.environment import Plane
from app.neat_training.evaluate import eval_genomes
from app.genetic_algorithm.train_deap import run_evolution
from app.utils.logger import get_logger
import neat

if __name__ == "__main__":
    main_logger = get_logger("main_logger")
    plane = Plane(1000, 1000, num_food=100)
    # plane.show_food()    
    
    # Run NEAT to train movement
    config_path = "app/neat_training/neat_config.txt"
    neat_population = neat.Population(neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                                  neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path))

    # Set up the reporter
    neat_population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    neat_population.add_reporter(stats)
    neat_population.add_reporter(neat.Checkpointer(150))

    winner = neat_population.run(eval_genomes, 1)
    main_logger.info(f"NEAT Winner: {winner}")

    # Save best model
    checkpoint = neat.Checkpointer()
    checkpoint.save_checkpoint(neat_population, neat_population.species, neat_population.generation, "neat_best_model")

    # Run Genetic Algorithm to evolve traits
    best_traits = run_evolution()
    main_logger.info(f"Best traits: {best_traits}")
