"""
Statistics tracker for Hand Cricket matches
"""

from typing import List, Dict, Any
import numpy as np


class StatisticsTracker:
    """
    Tracks and analyzes statistics across multiple matches
    """
    
    def __init__(self):
        self.matches: List[Dict[str, Any]] = []
        self.predictions: List[Dict[str, Any]] = []
    
    def add_match(self, match_data: Dict[str, Any]):
        """Add a completed match to statistics"""
        self.matches.append(match_data)
    
    def add_prediction(self, actual: int, predicted: int, confidence: float):
        """Record a prediction for accuracy tracking"""
        self.predictions.append({
            'actual': actual,
            'predicted': predicted,
            'confidence': confidence,
            'correct': actual == predicted
        })
    
    def get_win_rate(self, player: str = "ai") -> float:
        """
        Calculate win rate for a player
        
        Args:
            player: 'ai' or 'player'
        
        Returns:
            Win rate as a percentage
        """
        if not self.matches:
            return 0.0
        
        wins = sum(1 for m in self.matches if m.get('winner') == player)
        return (wins / len(self.matches)) * 100
    
    def get_average_score(self, player: str = "ai") -> float:
        """Get average score for a player"""
        if not self.matches:
            return 0.0
        
        key = f"{player}_score"
        scores = [m.get(key, 0) for m in self.matches]
        return np.mean(scores)
    
    def get_prediction_accuracy(self) -> float:
        """Calculate prediction accuracy"""
        if not self.predictions:
            return 0.0
        
        correct = sum(1 for p in self.predictions if p['correct'])
        return (correct / len(self.predictions)) * 100
    
    def get_move_frequency(self, player_history: List[int]) -> Dict[int, float]:
        """
        Calculate frequency distribution of moves
        
        Args:
            player_history: List of player moves
        
        Returns:
            Dictionary mapping move -> frequency percentage
        """
        if not player_history:
            return {i: 0.0 for i in range(1, 7)}
        
        frequencies = {}
        total = len(player_history)
        
        for move in range(1, 7):
            count = player_history.count(move)
            frequencies[move] = (count / total) * 100
        
        return frequencies
    
    def get_summary(self) -> Dict[str, Any]:
        """Get comprehensive statistics summary"""
        return {
            'total_matches': len(self.matches),
            'ai_win_rate': self.get_win_rate('ai'),
            'player_win_rate': self.get_win_rate('player'),
            'ai_avg_score': self.get_average_score('ai'),
            'player_avg_score': self.get_average_score('player'),
            'prediction_accuracy': self.get_prediction_accuracy(),
            'total_predictions': len(self.predictions)
        }
    
    def get_learning_curve(self, window_size: int = 10) -> List[float]:
        """
        Get prediction accuracy over time with moving average
        
        Args:
            window_size: Size of the moving average window
        
        Returns:
            List of accuracy percentages
        """
        if not self.predictions:
            return []
        
        accuracies = []
        for i in range(len(self.predictions)):
            start = max(0, i - window_size + 1)
            window = self.predictions[start:i+1]
            correct = sum(1 for p in window if p['correct'])
            accuracy = (correct / len(window)) * 100
            accuracies.append(accuracy)
        
        return accuracies
