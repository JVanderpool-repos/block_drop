"""
Game board logic for Tetris
"""

from typing import List, Optional, Set, Tuple
from .constants import BOARD_WIDTH, BOARD_HEIGHT, PIECE_COLORS
from .block_drop import BlockDrop


class Board:
    """Represents the Tetris game board"""
    
    def __init__(self, width: int = BOARD_WIDTH, height: int = BOARD_HEIGHT):
        self.width = width
        self.height = height
        # Grid stores the piece type at each position (None for empty)
        self.grid: List[List[Optional[str]]] = [[None for _ in range(width)] for _ in range(height)]
        self.cleared_lines = 0
    
    def is_valid_position(self, piece: BlockDrop) -> bool:
        """Check if a piece can be placed at its current position"""
        cells = piece.get_cells()
        
        for x, y in cells:
            # Check boundaries
            if x < 0 or x >= self.width or y >= self.height:
                return False
            
            # Check collision with existing pieces (only if y >= 0)
            if y >= 0 and self.grid[y][x] is not None:
                return False
        
        return True
    
    def place_piece(self, piece: BlockDrop) -> bool:
        """Place a piece on the board. Returns True if successful"""
        if not self.is_valid_position(piece):
            return False
        
        cells = piece.get_cells()
        for x, y in cells:
            if 0 <= y < self.height and 0 <= x < self.width:
                self.grid[y][x] = piece.piece_type
        
        return True
    
    def clear_lines(self) -> int:
        """Clear completed lines and return the number of lines cleared"""
        lines_to_clear = []
        
        # Find completed lines
        for y in range(self.height):
            if all(cell is not None for cell in self.grid[y]):
                lines_to_clear.append(y)
        
        # Remove completed lines
        for y in reversed(lines_to_clear):
            del self.grid[y]
            # Add new empty line at the top
            self.grid.insert(0, [None for _ in range(self.width)])
        
        lines_cleared = len(lines_to_clear)
        self.cleared_lines += lines_cleared
        return lines_cleared
    
    def is_game_over(self) -> bool:
        """Check if the game is over (pieces reach the top)"""
        # Check if any cell in the top row is occupied
        return any(cell is not None for cell in self.grid[0])
    
    def get_drop_position(self, piece: BlockDrop) -> int:
        """Get the Y position where the piece would land if dropped"""
        test_piece = piece.copy()
        
        while self.is_valid_position(test_piece):
            test_piece.y += 1
        
        return test_piece.y - 1
    
    def get_cell_type(self, x: int, y: int) -> Optional[str]:
        """Get the piece type at the given position"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
    
    def get_shadow_cells(self, piece: BlockDrop) -> List[Tuple[int, int]]:
        """Get the cells where the shadow (ghost) piece would be"""
        shadow_piece = piece.copy()
        shadow_piece.y = self.get_drop_position(piece)
        return shadow_piece.get_cells()
    
    def clear_board(self):
        """Clear the entire board"""
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.cleared_lines = 0
    
    def get_height_at_column(self, col: int) -> int:
        """Get the height of blocks in a given column"""
        for row in range(self.height):
            if self.grid[row][col] is not None:
                return self.height - row
        return 0
    
    def count_holes(self) -> int:
        """Count the number of empty cells with blocks above them"""
        holes = 0
        for col in range(self.width):
            block_found = False
            for row in range(self.height):
                if self.grid[row][col] is not None:
                    block_found = True
                elif block_found and self.grid[row][col] is None:
                    holes += 1
        return holes