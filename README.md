# Tetris Game

A classic Tetris implementation built with Python and Pygame.

## Features

- **Complete Tetris gameplay** with all 7 standard block drop pieces (I, O, T, S, Z, J, L)
- **Smooth piece movement** with gravity, rotation, and wall kicks
- **Line clearing** with proper scoring system
- **Level progression** with increasing speed
- **Next piece preview** 
- **Ghost piece** showing drop position
- **Pause functionality**
- **Game over and restart** capabilities
- **Clean, retro-style graphics**

## Controls

| Key | Action |
|-----|--------|
| ← → | Move piece left/right |
| ↓ | Soft drop (faster fall) |
| ↑ or X | Rotate piece clockwise |
| Z | Rotate piece counterclockwise |
| Space | Hard drop (instant drop) |
| P | Pause/Resume game |
| R | Restart game (when game over) |

## Installation

1. **Clone or download** this repository
2. **Install Python 3.7+** if not already installed
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

```bash
python main.py
```

## Project Structure

```
block_drop/
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── README.md           # This file
└── src/
    ├── __init__.py     # Package marker
    ├── constants.py    # Game constants and configuration
    ├── block_drop.py   # Tetris piece classes and logic
    ├── board.py        # Game board and collision detection
    ├── game.py         # Main game engine and logic
    └── renderer.py     # Pygame-based graphics rendering
```

## Game Rules

- **Objective:** Clear horizontal lines by filling them completely with blocks
- **Scoring:**
  - Single line: 100 × level
  - Double lines: 300 × level  
  - Triple lines: 500 × level
  - Tetris (4 lines): 800 × level
  - Soft drop: 1 point per cell
  - Hard drop: 2 points per cell
- **Level up:** Every 10 lines cleared
- **Speed:** Increases each level (pieces fall faster)
- **Game Over:** When pieces reach the top of the board

## Technical Details

- **Language:** Python 3.7+
- **Graphics:** Pygame 2.1.0+
- **Architecture:** Modular design with separate classes for game logic, rendering, and piece management
- **FPS:** 60 frames per second
- **Resolution:** 800×600 pixels

## Development

The game is built with a clean, modular architecture:

- `TetrisGame`: Main game loop and state management
- `Board`: Game board logic, collision detection, line clearing
- `BlockDrop`: Piece shapes, rotation, and movement
- `GameRenderer`: All graphics and UI rendering
- `BlockDropGenerator`: Random piece generation using bag system

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to fork this project and submit pull requests with improvements or bug fixes!

---

Enjoy playing Tetris! 🎮