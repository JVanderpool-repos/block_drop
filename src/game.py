"""
Main Tetris game engine
"""

import pygame
import time
from typing import Optional
from .constants import *
from .board import Board
from .block_drop import BlockDrop, BlockDropGenerator
from .renderer import GameRenderer


class TetrisGame:
    """Main Tetris game class"""
    
    def __init__(self):
        self.board = Board()
        self.piece_generator = BlockDropGenerator()
        self.renderer = GameRenderer()
        
        # Game state
        self.current_piece: Optional[BlockDrop] = None
        self.next_piece: Optional[BlockDrop] = None
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        
        # Timing
        self.last_fall_time = 0
        self.fall_speed = INITIAL_FALL_SPEED
        self.last_move_time = 0
        self.move_delay = MOVE_REPEAT_DELAY
        
        # Input state
        self.keys_pressed = set()
        self.key_repeat_timers = {}
        
        # Initialize first pieces
        self.spawn_new_piece()
        self.next_piece = self.piece_generator.get_next_piece()
    
    def spawn_new_piece(self):
        """Spawn a new piece at the top of the board"""
        if self.next_piece:
            self.current_piece = self.next_piece
            self.current_piece.x = BOARD_WIDTH // 2 - 1
            self.current_piece.y = 0
        else:
            self.current_piece = self.piece_generator.get_next_piece(BOARD_WIDTH // 2 - 1, 0)
        
        self.next_piece = self.piece_generator.get_next_piece()
        
        # Check for game over
        if not self.board.is_valid_position(self.current_piece):
            self.game_over = True
    
    def move_piece(self, dx: int, dy: int) -> bool:
        """Try to move the current piece. Returns True if successful"""
        if not self.current_piece or self.game_over or self.paused:
            return False
        
        # Create a copy to test the move
        test_piece = self.current_piece.copy()
        test_piece.move(dx, dy)
        
        if self.board.is_valid_position(test_piece):
            self.current_piece.move(dx, dy)
            return True
        
        return False
    
    def rotate_piece(self, clockwise: bool = True) -> bool:
        """Try to rotate the current piece. Returns True if successful"""
        if not self.current_piece or self.game_over or self.paused:
            return False
        
        # Create a copy to test the rotation
        test_piece = self.current_piece.copy()
        
        if clockwise:
            test_piece.rotate_clockwise()
        else:
            test_piece.rotate_counterclockwise()
        
        # Try the rotation at current position
        if self.board.is_valid_position(test_piece):
            if clockwise:
                self.current_piece.rotate_clockwise()
            else:
                self.current_piece.rotate_counterclockwise()
            return True
        
        # Try wall kicks (simple implementation)
        for dx in [-1, 1, -2, 2]:
            test_piece.x = self.current_piece.x + dx
            if self.board.is_valid_position(test_piece):
                if clockwise:
                    self.current_piece.rotate_clockwise()
                else:
                    self.current_piece.rotate_counterclockwise()
                self.current_piece.x += dx
                return True
            test_piece.x = self.current_piece.x  # Reset for next iteration
        
        return False
    
    def hard_drop(self):
        """Drop the piece all the way down"""
        if not self.current_piece or self.game_over or self.paused:
            return
        
        drop_distance = 0
        while self.move_piece(0, 1):
            drop_distance += 1
        
        # Add score for hard drop
        self.score += drop_distance * 2
        
        # Lock the piece immediately
        self.lock_piece()
    
    def soft_drop(self) -> bool:
        """Move piece down faster. Returns True if successful"""
        if self.move_piece(0, 1):
            self.score += SCORE_SOFT_DROP
            return True
        return False
    
    def lock_piece(self):
        """Lock the current piece in place and spawn a new one"""
        if not self.current_piece:
            return
        
        # Place the piece on the board
        self.board.place_piece(self.current_piece)
        
        # Clear completed lines
        lines_cleared = self.board.clear_lines()
        if lines_cleared > 0:
            self.lines_cleared += lines_cleared
            self.update_score(lines_cleared)
            self.update_level()
        
        # Check for game over
        if self.board.is_game_over():
            self.game_over = True
        else:
            # Spawn new piece
            self.spawn_new_piece()
    
    def update_score(self, lines_cleared: int):
        """Update score based on lines cleared"""
        base_score = 0
        if lines_cleared == 1:
            base_score = SCORE_SINGLE
        elif lines_cleared == 2:
            base_score = SCORE_DOUBLE
        elif lines_cleared == 3:
            base_score = SCORE_TRIPLE
        elif lines_cleared == 4:
            base_score = SCORE_TETRIS
        
        self.score += base_score * self.level
    
    def update_level(self):
        """Update level based on lines cleared"""
        new_level = 1 + self.lines_cleared // LINES_PER_LEVEL
        if new_level > self.level:
            self.level = new_level
            self.fall_speed = int(INITIAL_FALL_SPEED * (SPEED_INCREASE ** (self.level - 1)))
    
    def handle_input(self, events):
        """Handle input events"""
        current_time = pygame.time.get_ticks()
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                self.key_repeat_timers[event.key] = current_time + MOVE_REPEAT_DELAY
                
                # Handle immediate actions
                if event.key == pygame.K_UP or event.key == pygame.K_x:
                    self.rotate_piece(True)
                elif event.key == pygame.K_z:
                    self.rotate_piece(False)
                elif event.key == pygame.K_SPACE:
                    self.hard_drop()
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
            
            elif event.type == pygame.KEYUP:
                if event.key in self.keys_pressed:
                    self.keys_pressed.remove(event.key)
                if event.key in self.key_repeat_timers:
                    del self.key_repeat_timers[event.key]
        
        # Handle continuous movement
        if not self.paused and not self.game_over:
            for key in list(self.keys_pressed):
                if key in self.key_repeat_timers and current_time >= self.key_repeat_timers[key]:
                    if key == pygame.K_LEFT:
                        self.move_piece(-1, 0)
                    elif key == pygame.K_RIGHT:
                        self.move_piece(1, 0)
                    elif key == pygame.K_DOWN:
                        self.soft_drop()
                    
                    # Set next repeat time
                    self.key_repeat_timers[key] = current_time + MOVE_REPEAT_INTERVAL
    
    def update(self):
        """Update game state"""
        if self.game_over or self.paused:
            return
        
        current_time = pygame.time.get_ticks()
        
        # Handle piece falling
        if current_time - self.last_fall_time >= self.fall_speed:
            if not self.move_piece(0, 1):
                # Piece can't move down, lock it
                self.lock_piece()
            self.last_fall_time = current_time
    
    def restart_game(self):
        """Restart the game"""
        self.board.clear_board()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.paused = False
        self.fall_speed = INITIAL_FALL_SPEED
        
        # Reset pieces
        self.piece_generator = BlockDropGenerator()
        self.spawn_new_piece()
        self.next_piece = self.piece_generator.get_next_piece()
    
    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            
            self.handle_input(events)
            self.update()
            
            # Render
            self.renderer.render(self)
            
            clock.tick(60)  # 60 FPS