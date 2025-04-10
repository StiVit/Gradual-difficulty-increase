from app.utils.logger import get_logger
from app.visualization.visualization import visualize_game
from app.neat_training.run_neat import run_neat
from dotenv import load_dotenv
from app.utils.settings import settings

if __name__ == "__main__":
    main_logger = get_logger("main_logger")
    
    winner = run_neat()
    # Run Genetic Algorithm to evolve traits
    # best_traits = run_evolution()
    # main_logger.info(f"Best traits: {best_traits}")
    visualize_game(winner)
    main_logger.info("Game Over")
