from app.utils.logger import get_logger
from app.visualization.game import visualize_game
from app.neat_training.run_neat import run_neat

if __name__ == "__main__":
    main_logger = get_logger("main_logger")

    play = input("Would you like to play the game: y/n: ")
    if play not in ('y', 'n', 'Y', 'N'):
        raise ValueError("Invalid input")
    elif play in ['y', 'Y']:
        player_agent = True
    else:
        player_agent = False

    more_difficult = input("Would you like for the game to be more difficult? y/n: ")
    if more_difficult not in ('y', 'n', 'Y', 'N'):
        raise ValueError("Invalid input")
    elif more_difficult in ['y', 'Y']:
        difficulty_increase = True
    else:
        difficulty_increase = False
    
    winner = run_neat()
    # Run Genetic Algorithm to evolve traits
    # best_traits = run_evolution()
    # main_logger.info(f"Best traits: {best_traits}")
    visualize_game(winner, player_agent, difficulty_increase)
    main_logger.info("Game Over")
