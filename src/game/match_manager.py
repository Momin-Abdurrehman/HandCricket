"""
Match manager for organizing Hand Cricket matches
"""

from typing import Optional, Dict, Any
from .engine import GameEngine
from .player import Player


class MatchManager:
    """
    Manages the overall flow of a Hand Cricket match
    """
    
    def __init__(self, player: Player, ai_agent):
        self.player = player
        self.ai_agent = ai_agent
        self.engine = GameEngine()
        self.match_history: list = []
    
    def start_new_match(self, player_bats_first: Optional[bool] = None) -> Dict[str, Any]:
        """
        Start a new match
        
        Args:
            player_bats_first: If None, perform toss. Otherwise use given value.
        
        Returns:
            Dictionary with toss result
        """
        self.engine.reset()
        
        if player_bats_first is None:
            player_wins_toss = self.engine.toss()
        else:
            player_wins_toss = player_bats_first
        
        self.engine.player_batting = player_wins_toss
        
        return {
            'player_bats_first': player_wins_toss,
            'message': f"{'Player' if player_wins_toss else 'AI'} will bat first!"
        }
    
    def play_turn(self, player_move: int) -> Dict[str, Any]:
        """
        Play a single turn
        
        Args:
            player_move: The player's chosen number
        
        Returns:
            Dictionary with turn results
        """
        # Record player move
        self.player.make_move(player_move)
        
        # Get AI move
        is_batting = not self.engine.player_batting
        ai_move = self.ai_agent.choose_move(
            player_history=self.player.get_move_history(),
            is_batting=is_batting,
            current_score=self.engine.ai_score if is_batting else self.engine.player_score,
            opponent_score=self.engine.player_score if is_batting else self.engine.ai_score
        )
        
        # Process the turn
        is_out, runs, message = self.engine.play_turn(player_move, ai_move)
        
        # Update AI with the result
        self.ai_agent.update(player_move, is_out)
        
        # Check for innings switch
        turn_result = {
            'player_move': player_move,
            'ai_move': ai_move,
            'is_out': is_out,
            'runs': runs,
            'message': message,
            'innings_complete': False,
            'game_over': False
        }
        
        if is_out and self.engine.current_innings == 1:
            self.engine.switch_innings()
            turn_result['innings_complete'] = True
            turn_result['message'] += f"\nInnings over! Score: {self.engine.player_score if not self.engine.player_batting else self.engine.ai_score}"
        
        # Check if game is over
        if self.engine.check_game_over():
            turn_result['game_over'] = True
            turn_result['winner'] = self.engine.winner
            self._record_match()
        
        turn_result['game_state'] = self.engine.get_game_state()
        
        return turn_result
    
    def _record_match(self):
        """Record the completed match in history"""
        match_record = {
            'player_score': self.engine.player_score,
            'ai_score': self.engine.ai_score,
            'winner': self.engine.winner,
            'total_moves': len(self.engine.move_history),
            'move_history': self.engine.move_history.copy()
        }
        self.match_history.append(match_record)
    
    def get_match_history(self) -> list:
        """Get all completed matches"""
        return self.match_history.copy()
    
    def get_current_state(self) -> Dict[str, Any]:
        """Get current match state"""
        return self.engine.get_game_state()
