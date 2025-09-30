"""
Block Drop shapes and logic for Tetris pieces
"""

import random
from typing import List, Tuple

class BlockDrop:
    """Base class for all Tetris pieces"""
    
    # Define the basic shapes for each piece type
    SHAPES = {
        'I': [
            ['....', 'IIII', '....', '....'],
            ['..I.', '..I.', '..I.', '..I.'],
        ],
        'O': [
            ['OO', 'OO'],
        ],
        'T': [
            ['...', 'TTT', '.T.'],
            ['...', '.T.', 'TT.', '.T.'],
            ['...', '.T.', 'TTT', '...'],
            ['...', '.T.', '.TT', '.T.'],
        ],
        'S': [
            ['...', '.SS', 'SS.'],
            ['...', '.S.', '.SS', '..S'],
        ],
        'Z': [
            ['...', 'ZZ.', '.ZZ'],
            ['...', '..Z', '.ZZ', '.Z.'],
        ],
        'J': [
            ['...', 'JJJ', '..J'],
            ['...', '.J.', '.J.', 'JJ.'],
            ['...', 'J..', 'JJJ', '...'],
            ['...', '.JJ', '.J.', '.J.'],
        ],
        'L': [
            ['...', 'LLL', 'L..'],
            ['...', 'LL.', '.L.', '.L.'],
            ['...', '..L', 'LLL', '...'],
            ['...', '.L.', '.L.', '.LL'],
        ],
    }
    
    def __init__(self, piece_type: str, x: int = 0, y: int = 0):
        self.piece_type = piece_type
        self.x = x
        self.y = y
        self.rotation = 0
        self.shapes = self.SHAPES[piece_type]
    
    @property
    def current_shape(self) -> List[str]:
        """Get the current shape based on rotation"""
        return self.shapes[self.rotation % len(self.shapes)]
    
    def get_cells(self) -> List[Tuple[int, int]]:
        """Get the absolute positions of all cells occupied by this piece"""
        cells = []
        shape = self.current_shape
        
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell != '.' and cell != ' ':
                    cells.append((self.x + col_idx, self.y + row_idx))
        
        return cells
    
    def get_relative_cells(self) -> List[Tuple[int, int]]:
        """Get the relative positions of all cells occupied by this piece"""
        cells = []
        shape = self.current_shape
        
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell != '.' and cell != ' ':
                    cells.append((col_idx, row_idx))
        
        return cells
    
    def rotate_clockwise(self):
        """Rotate the piece clockwise"""
        self.rotation = (self.rotation + 1) % len(self.shapes)
    
    def rotate_counterclockwise(self):
        """Rotate the piece counterclockwise"""
        self.rotation = (self.rotation - 1) % len(self.shapes)
    
    def move(self, dx: int, dy: int):
        """Move the piece by the given offset"""
        self.x += dx
        self.y += dy
    
    def copy(self):
        """Create a copy of this piece"""
        new_piece = BlockDrop(self.piece_type, self.x, self.y)
        new_piece.rotation = self.rotation
        return new_piece
    
    def get_width(self) -> int:
        """Get the width of the current shape"""
        if not self.current_shape:
            return 0
        return len(self.current_shape[0])
    
    def get_height(self) -> int:
        """Get the height of the current shape"""
        return len(self.current_shape)


class BlockDropGenerator:
    """Generates random Tetris pieces"""
    
    PIECE_TYPES = ['I', 'O', 'T', 'S', 'Z', 'J', 'L']
    
    def __init__(self):
        self.bag = []
        self.refill_bag()
    
    def refill_bag(self):
        """Refill the bag with all piece types in random order"""
        self.bag = self.PIECE_TYPES.copy()
        random.shuffle(self.bag)
    
    def get_next_piece(self, x: int = 4, y: int = 0) -> BlockDrop:
        """Get the next piece from the bag"""
        if not self.bag:
            self.refill_bag()
        
        piece_type = self.bag.pop()
        return BlockDrop(piece_type, x, y)