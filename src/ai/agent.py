"""
Adaptive AI Agent - Integrates all three layers
"""

import numpy as np
from typing import List, Optional
from .pattern_mining import NGramModel, SlidingWindowAnalyzer, ExponentialMovingAverage, SequentialPatternDetector
from .predictive_learning import FTRLOptimizer, UCB1, OnlineLogisticRegression
from .decision_engine import MonteCarloSimulator


class AdaptiveAgent:
    """
    Main adaptive AI agent that integrates:
    - Layer 1: Pattern Mining
    - Layer 2: Predictive Learning
    - Layer 3: Strategic Decision Making
    """
    
    def __init__(self, use_all_layers: bool = True, difficulty: str = 'balanced'):
        """
        Initialize the adaptive agent
        
        Args:
            use_all_layers: If True, use all three layers. If False, use random strategy.
            difficulty: AI difficulty level - 'easy', 'balanced', or 'hard'
                       easy: More random, less accurate predictions
                       balanced: Default, fair gameplay
                       hard: More accurate predictions, smarter decisions
        """
        self.use_all_layers = use_all_layers
        self.difficulty = difficulty
        
        # Set difficulty parameters
        if difficulty == 'easy':
            self.randomness = 0.25  # 25% random moves
            self.learning_speed = 40  # Slower learning
            self.pattern_weight = 0.60  # Less pattern reliance
        elif difficulty == 'hard':
            self.randomness = 0.03  # 3% random moves
            self.learning_speed = 20  # Faster learning
            self.pattern_weight = 0.92  # High pattern reliance
        else:  # balanced
            self.randomness = 0.10  # 10% random moves
            self.learning_speed = 30  # Moderate learning
            self.pattern_weight = 0.82  # Balanced pattern reliance
        
        # Layer 1: Pattern Mining
        self.ngram_model = NGramModel(n=3)
        self.sliding_window = SlidingWindowAnalyzer(window_size=20)
        self.ema = ExponentialMovingAverage(alpha=0.3)
        self.pattern_detector = SequentialPatternDetector(min_support=2)
        
        # Layer 2: Predictive Learning
        self.ftrl = FTRLOptimizer(n_actions=6)
        self.ucb1 = UCB1(n_actions=6)
        self.online_lr = OnlineLogisticRegression(n_features=10, n_classes=6)
        
        # Layer 3: Strategic Decision
        self.monte_carlo = MonteCarloSimulator(n_simulations=1000)
        
        # Tracking
        self.move_history: List[int] = []
        self.prediction_history: List[int] = []
        self.confidence_scores: List[float] = []
        
    def choose_move(self, player_history: List[int], is_batting: bool,
                    current_score: int, opponent_score: int, 
                    innings: int = 1) -> int:
        """
        Choose the next move using the adaptive strategy
        
        Args:
            player_history: Complete history of player moves
            is_batting: Whether AI is batting
            current_score: AI's current score
            opponent_score: Opponent's current score
            innings: Current innings (1 or 2)
        
        Returns:
            Chosen move (1-6)
        """
        if not self.use_all_layers or len(player_history) < 3:
            # Not enough data or random mode - use simple strategy
            # Reduced threshold from 5 to 3 to start learning earlier
            return self._random_move()
        
        # Layer 1: Get predictions from pattern mining
        prob_dist = self._aggregate_pattern_predictions(player_history)
        
        # Store prediction for evaluation
        predicted_move = int(np.argmax(prob_dist)) + 1
        self.prediction_history.append(predicted_move)
        self.confidence_scores.append(float(np.max(prob_dist)))
        
        # Layer 3: Use Monte Carlo to choose best move
        # Add occasional randomness to prevent being too predictable
        if np.random.random() < self.randomness:
            # Occasionally make a random but reasonable move
            # Weighted towards safer moves (avoid extreme choices early)
            weights = 1.0 - prob_dist  # Inverse of predicted probabilities
            weights = weights / weights.sum()
            move = np.random.choice(range(1, 7), p=weights)
        else:
            move = self.monte_carlo.adaptive_strategy(
                prob_dist, is_batting, current_score, opponent_score, innings
            )
        
        return move
    
    def _aggregate_pattern_predictions(self, player_history: List[int]) -> np.ndarray:
        """
        Aggregate predictions from all pattern mining components
        
        Args:
            player_history: Complete history of player moves
        
        Returns:
            Combined probability distribution over moves 1-6
        """
        # Get predictions from each component
        ngram_probs = self.ngram_model.predict_probabilities(player_history[-5:])
        window_probs = self.sliding_window.get_frequency_distribution()
        ema_probs = self.ema.get_probabilities()
        pattern_probs = self.pattern_detector.predict_next(player_history[-5:])
        
        # Get predictions from learning algorithms
        ftrl_probs = self.ftrl.get_probabilities()
        ucb1_probs = self.ucb1.get_probabilities()
        
        # Extract features and get LR prediction
        features = self.online_lr.extract_features(player_history)
        lr_probs = self.online_lr.predict_probabilities(features)
        
        # Adaptive weighting based on game progress
        # Early game: less accurate predictions (more random)
        # Late game: more accurate predictions (learned patterns)
        history_length = len(player_history)
        learning_factor = min(1.0, history_length / self.learning_speed)  # Adaptive learning speed
        
        # Base uniform distribution for randomness
        uniform_probs = np.ones(6) / 6.0
        
        # Weighted combination with adaptive learning
        combined = (
            0.18 * ngram_probs +      # N-gram patterns (reduced from 0.20)
            0.12 * window_probs +      # Frequency in window (reduced from 0.15)
            0.15 * ema_probs +         # Exponential moving average (reduced from 0.20)
            0.12 * pattern_probs +     # Sequential patterns (reduced from 0.15)
            0.13 * ftrl_probs +        # FTRL learning (reduced from 0.15)
            0.08 * ucb1_probs +        # UCB1 exploration (reduced from 0.10)
            0.04 * lr_probs +          # Logistic regression (reduced from 0.05)
            0.18 * uniform_probs       # Random component for unpredictability
        )
        
        # Blend with uniform distribution based on learning progress
        # Early: more random, Late: more pattern-based
        blended = (learning_factor * self.pattern_weight) * combined + \
                  (1 - learning_factor * self.pattern_weight) * uniform_probs
        
        # Normalize
        return blended / blended.sum()
    
    def update(self, player_move: int, was_out: bool):
        """
        Update the agent with the outcome of a turn
        
        Args:
            player_move: The move the player made
            was_out: Whether the player got out
        """
        self.move_history.append(player_move)
        
        # Update Layer 1 components
        self.ngram_model.update([player_move])
        self.sliding_window.update(player_move)
        self.ema.update(player_move)
        self.pattern_detector.update([player_move], max_pattern_length=3)
        
        # Update Layer 2 components
        # FTRL: Update with loss (1 if predicted wrong, 0 if right)
        if len(self.prediction_history) > 0:
            predicted = self.prediction_history[-1]
            loss = 1.0 if predicted != player_move else 0.0
            self.ftrl.update(player_move - 1, loss)
        
        # UCB1: Update with reward (1 if predicted right, 0 otherwise)
        if len(self.prediction_history) > 0:
            predicted = self.prediction_history[-1]
            reward = 1.0 if predicted == player_move else 0.0
            self.ucb1.update(player_move - 1, reward)
        
        # Online LR: Update with true class
        if len(self.move_history) > 1:
            features = self.online_lr.extract_features(self.move_history[:-1])
            self.online_lr.update(features, player_move - 1)
    
    def _random_move(self) -> int:
        """Generate a random move"""
        return np.random.randint(1, 7)
    
    def get_prediction_accuracy(self) -> float:
        """
        Calculate prediction accuracy
        
        Returns:
            Accuracy percentage
        """
        if len(self.prediction_history) < 1 or len(self.move_history) < 1:
            return 0.0
        
        # Compare predictions with actual moves (offset by 1 since predictions are made before moves)
        min_len = min(len(self.prediction_history), len(self.move_history))
        correct = sum(1 for i in range(min_len) 
                     if self.prediction_history[i] == self.move_history[i])
        
        return (correct / min_len) * 100 if min_len > 0 else 0.0
    
    def get_statistics(self) -> dict:
        """Get agent statistics"""
        return {
            'total_predictions': len(self.prediction_history),
            'prediction_accuracy': self.get_prediction_accuracy(),
            'average_confidence': np.mean(self.confidence_scores) if self.confidence_scores else 0.0,
            'frequent_patterns': self.pattern_detector.get_frequent_patterns()[:5]
        }
    
    def reset(self):
        """Reset agent state for a new match"""
        self.move_history = []
        self.prediction_history = []
        self.confidence_scores = []
