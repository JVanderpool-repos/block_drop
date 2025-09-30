"""
Tetris Game - Main Entry Point
A classic Tetris implementation using Python and Pygame
"""

import pygame
import sys
from src.game import TetrisGame

def main():
    """Main function to initialize and run the Tetris game"""
    pygame.init()
    
    # Initialize the game
    game = TetrisGame()
    
    # Run the game
    game.run()
    
    # Quit
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()