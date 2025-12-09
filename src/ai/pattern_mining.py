"""
Pattern Mining Layer - Layer 1 of the AI system
Implements N-gram models, sliding window analysis, and sequential pattern detection
"""

from typing import List, Dict, Tuple
from collections import defaultdict, Counter
import numpy as np


class NGramModel:
    """
    N-gram sequence model for detecting player patterns
    Analyzes sequences of length 1, 2, and 3
    """
    
    def __init__(self, n: int = 3):
        """
        Initialize N-gram model
        
        Args:
            n: Maximum n-gram length (default: 3)
        """
        self.n = n
        self.ngrams = {i: defaultdict(Counter) for i in range(1, n + 1)}
    
    def update(self, sequence: List[int]):
        """
        Update n-gram counts with new sequence
        
        Args:
            sequence: List of moves
        """
        if not sequence:
            return
        
        # Update unigrams
        for move in sequence:
            self.ngrams[1][()][move] += 1
        
        # Update bigrams and trigrams
        for i in range(len(sequence)):
            for n_val in range(2, min(self.n + 1, i + 2)):
                if i >= n_val - 1:
                    prefix = tuple(sequence[i - n_val + 1:i])
                    current = sequence[i]
                    self.ngrams[n_val][prefix][current] += 1
    
    def predict_probabilities(self, recent_moves: List[int], smoothing: float = 0.1) -> np.ndarray:
        """
        Predict probability distribution for next move based on recent history
        
        Args:
            recent_moves: Recent move history
            smoothing: Laplace smoothing parameter
        
        Returns:
            Probability distribution over moves 1-6
        """
        probs = np.ones(6) * smoothing  # Laplace smoothing
        
        if not recent_moves:
            # Uniform distribution if no history
            return probs / probs.sum()
        
        # Try to use longest n-gram available
        for n_val in range(min(self.n, len(recent_moves)), 0, -1):
            prefix = tuple(recent_moves[-n_val:]) if n_val > 1 else ()
            
            if prefix in self.ngrams[n_val] or n_val == 1:
                counts = self.ngrams[n_val][prefix]
                if counts:
                    # Add counts to probabilities
                    for move in range(1, 7):
                        probs[move - 1] += counts[move]
                    break
        
        # Normalize
        return probs / probs.sum()


class SlidingWindowAnalyzer:
    """
    Analyzes frequency patterns in a sliding window of recent moves
    """
    
    def __init__(self, window_size: int = 20):
        """
        Initialize sliding window analyzer
        
        Args:
            window_size: Size of the sliding window
        """
        self.window_size = window_size
        self.move_history: List[int] = []
    
    def update(self, move: int):
        """Add a new move to the window"""
        self.move_history.append(move)
        if len(self.move_history) > self.window_size:
            self.move_history.pop(0)
    
    def get_frequency_distribution(self) -> np.ndarray:
        """
        Get frequency distribution of moves in the window
        
        Returns:
            Probability distribution over moves 1-6
        """
        if not self.move_history:
            return np.ones(6) / 6
        
        counts = np.zeros(6)
        for move in self.move_history:
            counts[move - 1] += 1
        
        # Add small smoothing
        counts += 0.01
        return counts / counts.sum()
    
    def detect_cycles(self) -> List[Tuple[List[int], int]]:
        """
        Detect cyclic patterns in the window
        
        Returns:
            List of (pattern, frequency) tuples
        """
        if len(self.move_history) < 4:
            return []
        
        patterns = []
        
        # Check for patterns of length 2-4
        for pattern_len in range(2, min(5, len(self.move_history) // 2 + 1)):
            pattern_counts = Counter()
            
            for i in range(len(self.move_history) - pattern_len + 1):
                pattern = tuple(self.move_history[i:i + pattern_len])
                pattern_counts[pattern] += 1
            
            # Report patterns that appear multiple times
            for pattern, count in pattern_counts.items():
                if count >= 2:
                    patterns.append((list(pattern), count))
        
        return patterns


class ExponentialMovingAverage:
    """
    Applies exponential weighting to give more importance to recent moves
    """
    
    def __init__(self, alpha: float = 0.3):
        """
        Initialize EMA
        
        Args:
            alpha: Smoothing factor (0-1), higher = more weight on recent data
        """
        self.alpha = alpha
        self.ema_probs = np.ones(6) / 6
    
    def update(self, move: int):
        """
        Update EMA with new move
        
        Args:
            move: The new move (1-6)
        """
        # Create one-hot vector for the move
        observation = np.zeros(6)
        observation[move - 1] = 1.0
        
        # Update EMA
        self.ema_probs = self.alpha * observation + (1 - self.alpha) * self.ema_probs
        
        # Renormalize
        self.ema_probs = self.ema_probs / self.ema_probs.sum()
    
    def get_probabilities(self) -> np.ndarray:
        """Get current EMA probability distribution"""
        return self.ema_probs.copy()


class SequentialPatternDetector:
    """
    Detects frequent sequential patterns (Mini-SPADE style)
    """
    
    def __init__(self, min_support: int = 2):
        """
        Initialize pattern detector
        
        Args:
            min_support: Minimum number of occurrences for a pattern to be frequent
        """
        self.min_support = min_support
        self.patterns: Dict[Tuple[int, ...], int] = defaultdict(int)
    
    def update(self, sequence: List[int], max_pattern_length: int = 3):
        """
        Update pattern database with new sequence
        
        Args:
            sequence: List of moves
            max_pattern_length: Maximum length of patterns to detect
        """
        # Extract all subsequences up to max_pattern_length
        for length in range(1, min(max_pattern_length + 1, len(sequence) + 1)):
            for i in range(len(sequence) - length + 1):
                pattern = tuple(sequence[i:i + length])
                self.patterns[pattern] += 1
    
    def get_frequent_patterns(self) -> List[Tuple[Tuple[int, ...], int]]:
        """
        Get all frequent patterns
        
        Returns:
            List of (pattern, count) tuples sorted by frequency
        """
        frequent = [(p, c) for p, c in self.patterns.items() if c >= self.min_support]
        return sorted(frequent, key=lambda x: x[1], reverse=True)
    
    def predict_next(self, recent_moves: List[int], top_k: int = 5) -> np.ndarray:
        """
        Predict next move based on matching patterns
        
        Args:
            recent_moves: Recent move history
            top_k: Number of top patterns to consider
        
        Returns:
            Probability distribution over moves 1-6
        """
        if not recent_moves:
            return np.ones(6) / 6
        
        probs = np.zeros(6)
        
        # Look for patterns that match the end of recent_moves
        for pattern_len in range(min(3, len(recent_moves)), 0, -1):
            suffix = tuple(recent_moves[-pattern_len:])
            
            # Find all patterns that start with this suffix
            matching_extensions = []
            for pattern, count in self.patterns.items():
                if len(pattern) == pattern_len + 1 and pattern[:-1] == suffix:
                    matching_extensions.append((pattern[-1], count))
            
            if matching_extensions:
                # Weight by frequency
                for move, count in matching_extensions:
                    probs[move - 1] += count
                break
        
        # If no patterns found, return uniform
        if probs.sum() == 0:
            return np.ones(6) / 6
        
        return probs / probs.sum()
