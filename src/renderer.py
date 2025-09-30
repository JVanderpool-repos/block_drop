"""
Pygame-based renderer for the Tetris game
"""

import pygame
from typing import TYPE_CHECKING, Optional, List, Tuple
from .constants import *

if TYPE_CHECKING:
    from .game import TetrisGame
    from .block_drop import BlockDrop


class GameRenderer:
    """Handles all rendering for the Tetris game"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        
        # Initialize fonts
        pygame.font.init()
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # Calculate board position (centered)
        self.board_start_x = (SCREEN_WIDTH - BOARD_WIDTH * CELL_SIZE) // 2 - 100
        self.board_start_y = (SCREEN_HEIGHT - BOARD_HEIGHT * CELL_SIZE) // 2
        
        # UI panel positions
        self.info_panel_x = self.board_start_x + BOARD_WIDTH * CELL_SIZE + 20
        self.next_piece_x = self.info_panel_x
        self.next_piece_y = self.board_start_y + 50
    
    def render(self, game: 'TetrisGame'):
        """Render the entire game"""
        # Clear screen
        self.screen.fill(COLORS['BLACK'])
        
        # Render game board
        self.render_board(game.board)
        
        # Render current piece
        if game.current_piece:
            self.render_piece(game.current_piece, alpha=255)
            
            # Render shadow/ghost piece
            self.render_shadow_piece(game.board, game.current_piece)
        
        # Render UI
        self.render_ui(game)
        
        # Render game over or pause overlay
        if game.game_over:
            self.render_game_over_overlay()
        elif game.paused:
            self.render_pause_overlay()
        
        # Update display
        pygame.display.flip()
    
    def render_board(self, board):
        """Render the game board with placed pieces"""
        # Draw board background
        board_rect = pygame.Rect(
            self.board_start_x - 2,
            self.board_start_y - 2,
            BOARD_WIDTH * CELL_SIZE + 4,
            BOARD_HEIGHT * CELL_SIZE + 4
        )
        pygame.draw.rect(self.screen, COLORS['WHITE'], board_rect, 2)
        
        # Draw board cells
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                cell_x = self.board_start_x + x * CELL_SIZE
                cell_y = self.board_start_y + y * CELL_SIZE
                
                piece_type = board.get_cell_type(x, y)
                if piece_type:
                    # Draw filled cell
                    color = PIECE_COLORS.get(piece_type, COLORS['WHITE'])
                    self.draw_cell(cell_x, cell_y, color)
                else:
                    # Draw empty cell
                    self.draw_empty_cell(cell_x, cell_y)
    
    def render_piece(self, piece: 'BlockDrop', alpha: int = 255):
        """Render a block drop piece"""
        color = PIECE_COLORS.get(piece.piece_type, COLORS['WHITE'])
        
        # Create surface with alpha for transparency effects
        if alpha < 255:
            temp_surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
            temp_surface.set_alpha(alpha)
            temp_surface.fill(color)
        
        cells = piece.get_cells()
        for x, y in cells:
            if 0 <= x < BOARD_WIDTH and y >= 0:  # Only render visible cells
                cell_x = self.board_start_x + x * CELL_SIZE
                cell_y = self.board_start_y + y * CELL_SIZE
                
                if alpha < 255:
                    self.screen.blit(temp_surface, (cell_x, cell_y))
                    # Draw border
                    pygame.draw.rect(self.screen, COLORS['GRAY'], 
                                   (cell_x, cell_y, CELL_SIZE, CELL_SIZE), 1)
                else:
                    self.draw_cell(cell_x, cell_y, color)
    
    def render_shadow_piece(self, board, piece: 'BlockDrop'):
        """Render the shadow/ghost piece showing where it will land"""
        shadow_cells = board.get_shadow_cells(piece)
        
        for x, y in shadow_cells:
            if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT:
                cell_x = self.board_start_x + x * CELL_SIZE
                cell_y = self.board_start_y + y * CELL_SIZE
                
                # Draw shadow as outline only
                pygame.draw.rect(self.screen, COLORS['GRAY'], 
                               (cell_x, cell_y, CELL_SIZE, CELL_SIZE), 1)
    
    def render_ui(self, game: 'TetrisGame'):
        """Render the UI elements"""
        # Score
        score_text = self.font_medium.render(f"Score: {game.score}", True, COLORS['WHITE'])
        self.screen.blit(score_text, (self.info_panel_x, self.board_start_y))
        
        # Level
        level_text = self.font_medium.render(f"Level: {game.level}", True, COLORS['WHITE'])
        self.screen.blit(level_text, (self.info_panel_x, self.board_start_y + 30))
        
        # Lines cleared
        lines_text = self.font_medium.render(f"Lines: {game.lines_cleared}", True, COLORS['WHITE'])
        self.screen.blit(lines_text, (self.info_panel_x, self.board_start_y + 60))
        
        # Next piece
        if game.next_piece:
            self.render_next_piece(game.next_piece)
        
        # Controls help
        self.render_controls_help()
    
    def render_next_piece(self, next_piece: 'BlockDrop'):
        """Render the next piece preview"""
        # Title
        next_text = self.font_medium.render("Next:", True, COLORS['WHITE'])
        self.screen.blit(next_text, (self.next_piece_x, self.next_piece_y))
        
        # Background box
        preview_width = 5 * CELL_SIZE // 2
        preview_height = 4 * CELL_SIZE // 2
        preview_rect = pygame.Rect(
            self.next_piece_x,
            self.next_piece_y + 30,
            preview_width,
            preview_height
        )
        pygame.draw.rect(self.screen, COLORS['DARK_GRAY'], preview_rect)
        pygame.draw.rect(self.screen, COLORS['WHITE'], preview_rect, 1)
        
        # Render the piece (scaled down)
        color = PIECE_COLORS.get(next_piece.piece_type, COLORS['WHITE'])
        shape = next_piece.current_shape
        cell_size = CELL_SIZE // 2
        
        # Center the piece in the preview
        start_x = self.next_piece_x + (preview_width - len(shape[0]) * cell_size) // 2
        start_y = self.next_piece_y + 30 + (preview_height - len(shape) * cell_size) // 2
        
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell != '.' and cell != ' ':
                    cell_x = start_x + col_idx * cell_size
                    cell_y = start_y + row_idx * cell_size
                    
                    pygame.draw.rect(self.screen, color, 
                                   (cell_x, cell_y, cell_size, cell_size))
                    pygame.draw.rect(self.screen, COLORS['WHITE'], 
                                   (cell_x, cell_y, cell_size, cell_size), 1)
    
    def render_controls_help(self):
        """Render control instructions"""
        help_y = self.next_piece_y + 150
        controls = [
            "Controls:",
            "← → Move",
            "↓ Soft Drop",
            "↑/X Rotate",
            "Z Counter-rotate",
            "Space Hard Drop",
            "P Pause",
            "R Restart (Game Over)"
        ]
        
        for i, text in enumerate(controls):
            color = COLORS['YELLOW'] if i == 0 else COLORS['WHITE']
            font = self.font_medium if i == 0 else self.font_small
            rendered_text = font.render(text, True, color)
            self.screen.blit(rendered_text, (self.info_panel_x, help_y + i * 20))
    
    def render_game_over_overlay(self):
        """Render game over screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(COLORS['BLACK'])
        self.screen.blit(overlay, (0, 0))
        
        # Game over text
        game_over_text = self.font_large.render("GAME OVER", True, COLORS['RED'])
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, text_rect)
        
        # Restart instruction
        restart_text = self.font_medium.render("Press R to restart", True, COLORS['WHITE'])
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(restart_text, restart_rect)
    
    def render_pause_overlay(self):
        """Render pause screen"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(COLORS['BLACK'])
        self.screen.blit(overlay, (0, 0))
        
        # Paused text
        paused_text = self.font_large.render("PAUSED", True, COLORS['YELLOW'])
        text_rect = paused_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 25))
        self.screen.blit(paused_text, text_rect)
        
        # Resume instruction
        resume_text = self.font_medium.render("Press P to resume", True, COLORS['WHITE'])
        resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25))
        self.screen.blit(resume_text, resume_rect)
    
    def draw_cell(self, x: int, y: int, color: Tuple[int, int, int]):
        """Draw a filled cell with border"""
        # Fill
        pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
        
        # Border
        pygame.draw.rect(self.screen, COLORS['WHITE'], (x, y, CELL_SIZE, CELL_SIZE), 1)
        
        # Highlight effect (lighter color on top/left edges)
        lighter_color = tuple(min(255, c + 40) for c in color)
        pygame.draw.line(self.screen, lighter_color, (x, y), (x + CELL_SIZE - 1, y))
        pygame.draw.line(self.screen, lighter_color, (x, y), (x, y + CELL_SIZE - 1))
        
        # Shadow effect (darker color on bottom/right edges)
        darker_color = tuple(max(0, c - 40) for c in color)
        pygame.draw.line(self.screen, darker_color, (x + CELL_SIZE - 1, y), (x + CELL_SIZE - 1, y + CELL_SIZE - 1))
        pygame.draw.line(self.screen, darker_color, (x, y + CELL_SIZE - 1), (x + CELL_SIZE - 1, y + CELL_SIZE - 1))
    
    def draw_empty_cell(self, x: int, y: int):
        """Draw an empty cell"""
        pygame.draw.rect(self.screen, COLORS['DARK_GRAY'], (x, y, CELL_SIZE, CELL_SIZE), 1)