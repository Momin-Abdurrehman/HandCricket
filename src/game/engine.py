"""
Core game engine for Hand Cricket
"""

from typing import Optional, Tuple
import random


class GameEngine:
    """
    Core game engine that manages the rules and flow of Hand Cricket
    """
    
    def __init__(self):
        self.valid_moves = [1, 2, 3, 4, 5, 6]
        self.reset()
    
    def reset(self):
        """Reset the game state"""
        self.player_score = 0
        self.ai_score = 0
        self.player_batting = None
        self.current_innings = 1
        self.game_over = False
        self.winner = None
        self.move_history = []
        self.out_occurred = False
    
    def toss(self) -> bool:
        """
        Perform toss to decide who bats first
        Returns: True if player wins toss, False if AI wins
        """
        return random.choice([True, False])
    
    def is_valid_move(self, move: int) -> bool:
        """Check if a move is valid (1-6)"""
        return move in self.valid_moves
    
    def play_turn(self, player_move: int, ai_move: int) -> Tuple[bool, int, str]:
        """
        Process a single turn of the game
        
        Args:
            player_move: Player's chosen number (1-6)
            ai_move: AI's chosen number (1-6)
        
        Returns:
            Tuple of (is_out, runs_scored, message)
        """
        if not self.is_valid_move(player_move) or not self.is_valid_move(ai_move):
            raise ValueError("Invalid move. Choose a number between 1 and 6.")
        
        # Record the move
        self.move_history.append({
            'player_move': player_move,
            'ai_move': ai_move,
            'batting': 'player' if self.player_batting else 'ai',
            'innings': self.current_innings
        })
        
        # Check if moves match (out!)
        if player_move == ai_move:
            self.out_occurred = True
            return True, 0, "OUT!"
        
        # Calculate runs based on who's batting
        if self.player_batting:
            runs = player_move
            self.player_score += runs
            message = f"Player scores {runs} run(s)!"
        else:
            runs = ai_move
            self.ai_score += runs
            message = f"AI scores {runs} run(s)!"
        
        self.out_occurred = False
        return False, runs, message
    
    def switch_innings(self):
        """Switch between innings"""
        self.current_innings = 2
        self.player_batting = not self.player_batting
        self.out_occurred = False
    
    def check_game_over(self) -> bool:
        """
        Check if the game is over
        Returns: True if game is complete
        """
        if self.current_innings == 1 and self.out_occurred:
            return False
        
        if self.current_innings == 2:
            if self.out_occurred:
                self.game_over = True
                self._determine_winner()
                return True
            
            # Check if target is chased
            if self.player_batting and self.player_score > self.ai_score:
                self.game_over = True
                self._determine_winner()
                return True
            elif not self.player_batting and self.ai_score > self.player_score:
                self.game_over = True
                self._determine_winner()
                return True
        
        return False
    
    def _determine_winner(self):
        """Determine the winner of the match"""
        if self.player_score > self.ai_score:
            self.winner = "player"
        elif self.ai_score > self.player_score:
            self.winner = "ai"
        else:
            self.winner = "tie"
    
    def get_target(self) -> Optional[int]:
        """Get the target score for second innings"""
        if self.current_innings == 2:
            if self.player_batting:
                return self.ai_score + 1
            else:
                return self.player_score + 1
        return None
    
    def get_game_state(self) -> dict:
        """Get current game state"""
        return {
            'player_score': self.player_score,
            'ai_score': self.ai_score,
            'player_batting': self.player_batting,
            'current_innings': self.current_innings,
            'game_over': self.game_over,
            'winner': self.winner,
            'target': self.get_target(),
            'total_moves': len(self.move_history)
        }
