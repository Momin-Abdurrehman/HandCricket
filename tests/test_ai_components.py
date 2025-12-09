"""
Unit tests for AI components
"""

import unittest
import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ai import (AdaptiveAgent, NGramModel, SlidingWindowAnalyzer,
                    ExponentialMovingAverage, SequentialPatternDetector,
                    FTRLOptimizer, UCB1, OnlineLogisticRegression,
                    MonteCarloSimulator)


class TestNGramModel(unittest.TestCase):
    """Test N-gram model"""
    
    def setUp(self):
        self.model = NGramModel(n=3)
    
    def test_initialization(self):
        """Test model initializes correctly"""
        self.assertEqual(self.model.n, 3)
    
    def test_update(self):
        """Test model updates with sequences"""
        sequence = [1, 2, 3, 4]
        self.model.update(sequence)
        
        # Check that counts were updated
        self.assertGreater(len(self.model.ngrams[1][()]), 0)
    
    def test_predict_probabilities(self):
        """Test probability prediction"""
        # Train with repeated pattern
        for _ in range(10):
            self.model.update([1, 2, 3])
        
        probs = self.model.predict_probabilities([1, 2])
        
        # Should be a valid probability distribution
        self.assertEqual(len(probs), 6)
        self.assertAlmostEqual(np.sum(probs), 1.0, places=5)
        self.assertTrue(np.all(probs >= 0))


class TestSlidingWindowAnalyzer(unittest.TestCase):
    """Test sliding window analyzer"""
    
    def setUp(self):
        self.analyzer = SlidingWindowAnalyzer(window_size=10)
    
    def test_update(self):
        """Test window updates correctly"""
        for i in range(15):
            self.analyzer.update(1)
        
        # Should only keep last 10
        self.assertEqual(len(self.analyzer.move_history), 10)
    
    def test_frequency_distribution(self):
        """Test frequency distribution calculation"""
        # Add known sequence
        for _ in range(5):
            self.analyzer.update(1)
        for _ in range(3):
            self.analyzer.update(2)
        
        dist = self.analyzer.get_frequency_distribution()
        
        self.assertEqual(len(dist), 6)
        self.assertAlmostEqual(np.sum(dist), 1.0, places=5)


class TestExponentialMovingAverage(unittest.TestCase):
    """Test EMA"""
    
    def setUp(self):
        self.ema = ExponentialMovingAverage(alpha=0.5)
    
    def test_update(self):
        """Test EMA updates"""
        self.ema.update(3)
        probs = self.ema.get_probabilities()
        
        self.assertEqual(len(probs), 6)
        self.assertAlmostEqual(np.sum(probs), 1.0, places=5)


class TestFTRLOptimizer(unittest.TestCase):
    """Test FTRL optimizer"""
    
    def setUp(self):
        self.ftrl = FTRLOptimizer(n_actions=6)
    
    def test_initialization(self):
        """Test FTRL initializes correctly"""
        self.assertEqual(self.ftrl.n_actions, 6)
    
    def test_update(self):
        """Test FTRL updates weights"""
        initial_w = self.ftrl.w.copy()
        self.ftrl.update(2, 0.5)
        
        # Weights should change
        self.assertFalse(np.array_equal(initial_w, self.ftrl.w))
    
    def test_get_probabilities(self):
        """Test probability generation"""
        probs = self.ftrl.get_probabilities()
        
        self.assertEqual(len(probs), 6)
        self.assertAlmostEqual(np.sum(probs), 1.0, places=5)
        self.assertTrue(np.all(probs >= 0))


class TestUCB1(unittest.TestCase):
    """Test UCB1 algorithm"""
    
    def setUp(self):
        self.ucb = UCB1(n_actions=6)
    
    def test_select_action(self):
        """Test action selection"""
        action = self.ucb.select_action()
        self.assertIn(action, range(6))
    
    def test_update(self):
        """Test update mechanism"""
        self.ucb.update(2, 1.0)
        self.assertEqual(self.ucb.counts[2], 1)
        self.assertEqual(self.ucb.values[2], 1.0)


class TestMonteCarloSimulator(unittest.TestCase):
    """Test Monte Carlo simulator"""
    
    def setUp(self):
        self.simulator = MonteCarloSimulator(n_simulations=100)
    
    def test_evaluate_move(self):
        """Test move evaluation"""
        prob_dist = np.ones(6) / 6  # Uniform distribution
        
        expected_runs, risk = self.simulator.evaluate_move(
            move=3,
            opponent_prob_dist=prob_dist,
            is_batting=True,
            current_score=10,
            opponent_score=8
        )
        
        # Risk should be between 0 and 1
        self.assertGreaterEqual(risk, 0)
        self.assertLessEqual(risk, 1)
    
    def test_choose_best_move(self):
        """Test best move selection"""
        prob_dist = np.ones(6) / 6
        
        move = self.simulator.choose_best_move(
            opponent_prob_dist=prob_dist,
            is_batting=True,
            current_score=10,
            opponent_score=8
        )
        
        self.assertIn(move, range(1, 7))


class TestAdaptiveAgent(unittest.TestCase):
    """Test adaptive agent"""
    
    def setUp(self):
        self.agent = AdaptiveAgent(use_all_layers=True)
    
    def test_initialization(self):
        """Test agent initializes correctly"""
        self.assertIsNotNone(self.agent.ngram_model)
        self.assertIsNotNone(self.agent.monte_carlo)
    
    def test_choose_move(self):
        """Test move selection"""
        # Provide some history
        player_history = [1, 2, 3, 4, 5, 6, 1, 2]
        
        move = self.agent.choose_move(
            player_history=player_history,
            is_batting=True,
            current_score=10,
            opponent_score=8
        )
        
        self.assertIn(move, range(1, 7))
    
    def test_update(self):
        """Test agent update mechanism"""
        initial_history_len = len(self.agent.move_history)
        
        self.agent.update(3, False)
        
        self.assertEqual(len(self.agent.move_history), initial_history_len + 1)
    
    def test_random_mode(self):
        """Test agent in random mode"""
        agent = AdaptiveAgent(use_all_layers=False)
        
        move = agent.choose_move(
            player_history=[1, 2, 3],
            is_batting=True,
            current_score=0,
            opponent_score=0
        )
        
        self.assertIn(move, range(1, 7))


if __name__ == '__main__':
    unittest.main()
