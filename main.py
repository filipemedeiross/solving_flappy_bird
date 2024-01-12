from argparse import ArgumentParser
from flappy_bean import FlappyBean


# Getting the command line arguments
parser = ArgumentParser(description='Game options')
parser.add_argument('--data-path')
args = parser.parse_args()

# Testing the game
game = FlappyBean(data_path=args.data_path)
game.init_game()
