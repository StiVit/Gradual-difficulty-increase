from app.neat_training.evaluate import eval_genomes
from app.utils.logger import get_logger
from app.neat_training.load_checkpoint import load_checkpoint
import neat
import os
import pickle

def run_neat():
    """
    Run NEAT to train movement.
    """
    neat_logger = get_logger("neat_logger")

    # Load a checkpoint if there is a player fitness file
    player_data_path = "player_fitness.txt"
    if os.path.exists(player_data_path):
        neat_logger.info("Loading checkpoint that fits the player performance model...")
        return load_checkpoint(player_data_path)
    
    # Initialize the population of neat
    config_path = "app/neat_training/neat_config.txt"
    neat_population = neat.Population(neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                                  neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path))

    # Set up the reporter
    # Create a custom folder for checkpoints if it doesn't exist
    checkpoint_dir = "checkpoints"
    os.makedirs(checkpoint_dir, exist_ok=True)

    # Add reporter for stat tracking
    neat_population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    neat_population.add_reporter(stats)
    neat_population.add_reporter(neat.Checkpointer(50, filename_prefix=os.path.join(checkpoint_dir, "neat_checkpoint_")))

    # If there is already a winner genome, load, otherwise train the AI again
    best_model_path = "app/neat_training/winner.pkl"
    if os.path.exists(best_model_path):
        neat_logger.info("Best model checkpoint found. Loading model...")
        # Load the best model from the saved file
        with open(best_model_path, "rb") as f:
            winner = pickle.load(f)
    else:
        neat_logger.info("No best model checkpoint found. Running NEAT population...")
        winner = neat_population.run(eval_genomes, 1000)
        # Save the best model to a file
        with open(best_model_path, "wb") as f:
            pickle.dump(winner, f)
        neat_logger.info(f"NEAT Winner: {winner}")
    
    return winner