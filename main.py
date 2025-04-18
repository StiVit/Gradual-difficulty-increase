from app.utils.logger import get_logger
from app.visualization.visualization import visualize_game
from app.neat_training.run_neat import run_neat

if __name__ == "__main__":
    main_logger = get_logger("main_logger")

    play = input("Would you like to play the game: y/n: ")
    if play not in ('y', 'n', 'Y', 'N'):
        raise ValueError("Invalid input")
    
    winner = run_neat()
    # Run Genetic Algorithm to evolve traits
    # best_traits = run_evolution()
    # main_logger.info(f"Best traits: {best_traits}")
    visualize_game(winner)
    main_logger.info("Game Over")
