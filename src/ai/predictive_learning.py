"""
Predictive Learning Layer - Layer 2 of the AI system
Implements FTRL, UCB1, and Online Logistic Regression
"""

import numpy as np
from typing import List


class FTRLOptimizer:
    """
    Follow-The-Regularized-Leader (FTRL) optimizer
    Used in online learning to update predictions based on errors
    """
    
    def __init__(self, n_actions: int = 6, alpha: float = 0.1, beta: float = 1.0, 
                 lambda1: float = 0.1, lambda2: float = 1.0):
        """
        Initialize FTRL optimizer
        
        Args:
            n_actions: Number of possible actions (6 for hand cricket)
            alpha: Learning rate
            beta: Per-coordinate learning rate
            lambda1: L1 regularization
            lambda2: L2 regularization
        """
        self.n_actions = n_actions
        self.alpha = alpha
        self.beta = beta
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        
        # FTRL state variables
        self.z = np.zeros(n_actions)  # Accumulated gradients
        self.n = np.zeros(n_actions)  # Squared gradient accumulator
        self.w = np.zeros(n_actions)  # Weights
    
    def update(self, action: int, loss: float):
        """
        Update weights based on observed loss
        
        Args:
            action: The action taken (0-5 for moves 1-6)
            loss: The loss incurred
        """
        # Compute gradient (simplified for single action)
        gradient = np.zeros(self.n_actions)
        gradient[action] = loss
        
        # Update accumulators
        sigma = (np.sqrt(self.n + gradient ** 2) - np.sqrt(self.n)) / self.alpha
        self.z += gradient - sigma * self.w
        self.n += gradient ** 2
        
        # Update weights using FTRL update rule
        for i in range(self.n_actions):
            if abs(self.z[i]) <= self.lambda1:
                self.w[i] = 0
            else:
                self.w[i] = -(self.z[i] - np.sign(self.z[i]) * self.lambda1) / \
                           ((self.beta + np.sqrt(self.n[i])) / self.alpha + self.lambda2)
    
    def get_probabilities(self) -> np.ndarray:
        """
        Get probability distribution over actions
        
        Returns:
            Softmax probability distribution
        """
        # Apply softmax to weights
        exp_w = np.exp(self.w - np.max(self.w))  # Numerical stability
        return exp_w / exp_w.sum()


class UCB1:
    """
    Upper Confidence Bound (UCB1) algorithm
    Balances exploration and exploitation
    """
    
    def __init__(self, n_actions: int = 6, c: float = 2.0):
        """
        Initialize UCB1
        
        Args:
            n_actions: Number of possible actions
            c: Exploration parameter (higher = more exploration)
        """
        self.n_actions = n_actions
        self.c = c
        
        # Action statistics
        self.counts = np.zeros(n_actions)  # Times each action was selected
        self.values = np.zeros(n_actions)  # Average reward for each action
        self.total_count = 0
    
    def select_action(self) -> int:
        """
        Select action using UCB1 formula
        
        Returns:
            Selected action index (0-5)
        """
        self.total_count += 1
        
        # Initially, try each action once
        if self.total_count <= self.n_actions:
            return self.total_count - 1
        
        # Compute UCB values
        ucb_values = np.zeros(self.n_actions)
        for i in range(self.n_actions):
            if self.counts[i] == 0:
                return i  # Try unexplored actions
            
            exploration_term = self.c * np.sqrt(np.log(self.total_count) / self.counts[i])
            ucb_values[i] = self.values[i] + exploration_term
        
        return int(np.argmax(ucb_values))
    
    def update(self, action: int, reward: float):
        """
        Update action statistics with observed reward
        
        Args:
            action: The action taken (0-5)
            reward: The reward received (higher is better)
        """
        self.counts[action] += 1
        # Incremental average update
        n = self.counts[action]
        self.values[action] = ((n - 1) * self.values[action] + reward) / n
    
    def get_probabilities(self) -> np.ndarray:
        """
        Get probability distribution based on current value estimates
        
        Returns:
            Softmax distribution over actions
        """
        if self.total_count == 0:
            return np.ones(self.n_actions) / self.n_actions
        
        # Softmax over values with exploration bonus
        ucb_values = np.zeros(self.n_actions)
        for i in range(self.n_actions):
            if self.counts[i] > 0:
                exploration = self.c * np.sqrt(np.log(self.total_count) / self.counts[i])
                ucb_values[i] = self.values[i] + exploration
            else:
                ucb_values[i] = float('inf')  # High value for unexplored
        
        # Convert to probabilities (handle inf case)
        if np.any(np.isinf(ucb_values)):
            probs = np.zeros(self.n_actions)
            probs[np.isinf(ucb_values)] = 1.0
            return probs / probs.sum()
        
        exp_values = np.exp(ucb_values - np.max(ucb_values))
        return exp_values / exp_values.sum()


class OnlineLogisticRegression:
    """
    Online Logistic Regression for multi-class prediction
    Updates weights incrementally as new data arrives
    """
    
    def __init__(self, n_features: int = 10, n_classes: int = 6, learning_rate: float = 0.01):
        """
        Initialize online logistic regression
        
        Args:
            n_features: Number of input features
            n_classes: Number of output classes (6 for moves 1-6)
            learning_rate: Learning rate for gradient descent
        """
        self.n_features = n_features
        self.n_classes = n_classes
        self.learning_rate = learning_rate
        
        # Initialize weights (small random values)
        self.weights = np.random.randn(n_features, n_classes) * 0.01
        self.bias = np.zeros(n_classes)
    
    def _softmax(self, logits: np.ndarray) -> np.ndarray:
        """Compute softmax probabilities"""
        exp_logits = np.exp(logits - np.max(logits))
        return exp_logits / exp_logits.sum()
    
    def predict_probabilities(self, features: np.ndarray) -> np.ndarray:
        """
        Predict probability distribution
        
        Args:
            features: Feature vector of shape (n_features,)
        
        Returns:
            Probability distribution over classes
        """
        logits = np.dot(features, self.weights) + self.bias
        return self._softmax(logits)
    
    def update(self, features: np.ndarray, true_class: int):
        """
        Update weights based on observed outcome
        
        Args:
            features: Feature vector of shape (n_features,)
            true_class: True class label (0-5 for moves 1-6)
        """
        # Get current predictions
        probs = self.predict_probabilities(features)
        
        # Create one-hot target
        target = np.zeros(self.n_classes)
        target[true_class] = 1.0
        
        # Compute gradient
        error = probs - target
        
        # Update weights
        self.weights -= self.learning_rate * np.outer(features, error)
        self.bias -= self.learning_rate * error
    
    def extract_features(self, move_history: List[int], max_history: int = 10) -> np.ndarray:
        """
        Extract features from move history
        
        Args:
            move_history: List of recent moves
            max_history: Maximum number of recent moves to use
        
        Returns:
            Feature vector
        """
        features = np.zeros(self.n_features)
        
        if not move_history:
            return features
        
        # Use most recent moves as features
        recent = move_history[-max_history:]
        for i, move in enumerate(recent):
            if i < self.n_features:
                features[i] = move / 6.0  # Normalize to [0, 1]
        
        return features
