import neat
from app.neat_training.evaluate import eval_genomes

__checkpoint_fitness_map = {
    0: "neat_checkpoint_49",
    50: "neat_checkpoint_99",
    100: "neat_checkpoint_149",
    250: "neat_checkpoint_299",
    350: "neat_checkpoint_499",
    450: "neat_checkpoint_699"
}

def load_checkpoint(player_data_path):
    with open(player_data_path, 'r') as file:
        fitness = int(file.readlines()[-1].strip())
    
    checkpoint_path = None
    for start_fitness, checkpoint in sorted(__checkpoint_fitness_map.items()):
        if fitness >= start_fitness:
            checkpoint_path = f"app/neat_training/checkpoints/{checkpoint}"
        else:
            break
    
    if checkpoint_path:
        pop = neat.Checkpointer.restore_checkpoint(checkpoint_path)
    else:
        raise ValueError("No suitable checkpoint found for the given fitness.")
    
    winner = pop.run(eval_genomes, 1)
    return winner