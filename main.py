from app.simulation.environment import Plane
from app.neat_training.evaluate import eval_genomes
from app.genetic_algorithm.train_deap import run_evolution
from app.utils.logger import get_logger
from app.visualization.show_food import show_food
import neat
import os

if __name__ == "__main__":
    main_logger = get_logger("main_logger")
    plane = Plane(1000, 1000, num_food=100)
    show_food(plane) 
    
    # Run NEAT to train movement
    config_path = "app/neat_training/neat_config.txt"
    neat_population = neat.Population(neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                                  neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path))

    # Set up the reporter
    # Create a custom folder for checkpoints if it doesn't exist
    checkpoint_dir = "app/neat_training/checkpoints"
    os.makedirs(checkpoint_dir, exist_ok=True)

    neat_population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    neat_population.add_reporter(stats)
    neat_population.add_reporter(neat.Checkpointer(10, filename_prefix=os.path.join(checkpoint_dir, "neat_checkpoint_")))

    winner = neat_population.run(eval_genomes, 100)
    main_logger.info(f"NEAT Winner: {winner}")

    # Save best model
    checkpoint = neat.Checkpointer()
    checkpoint.save_checkpoint(neat_population, neat_population.species, neat_population.generation, "neat_best_model")

    # Run Genetic Algorithm to evolve traits
    best_traits = run_evolution()
    main_logger.info(f"Best traits: {best_traits}")
