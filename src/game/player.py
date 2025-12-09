"""
Player class for Hand Cricket
"""

from typing import List


class Player:
    """
    Represents a human player in the game
    """
    
    def __init__(self, name: str = "Player"):
        self.name = name
        self.move_history: List[int] = []
    
    def make_move(self, move: int) -> int:
        """
        Record and return a player move
        
        Args:
            move: The number chosen by the player (1-6)
        
        Returns:
            The move value
        """
        if not isinstance(move, int) or move < 1 or move > 6:
            raise ValueError("Move must be an integer between 1 and 6")
        
        self.move_history.append(move)
        return move
    
    def get_move_history(self) -> List[int]:
        """Get the player's move history"""
        return self.move_history.copy()
    
    def reset_history(self):
        """Reset the player's move history"""
        self.move_history = []
