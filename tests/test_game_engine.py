"""
Unit tests for game engine components
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game import GameEngine, Player, MatchManager, StatisticsTracker
from src.ai import AdaptiveAgent


class TestGameEngine(unittest.TestCase):
    """Test GameEngine class"""
    
    def setUp(self):
        self.engine = GameEngine()
    
    def test_initialization(self):
        """Test engine initializes correctly"""
        self.assertEqual(self.engine.player_score, 0)
        self.assertEqual(self.engine.ai_score, 0)
        self.assertIsNone(self.engine.player_batting)
        self.assertFalse(self.engine.game_over)
    
    def test_valid_moves(self):
        """Test move validation"""
        for move in range(1, 7):
            self.assertTrue(self.engine.is_valid_move(move))
        
        self.assertFalse(self.engine.is_valid_move(0))
        self.assertFalse(self.engine.is_valid_move(7))
    
    def test_play_turn_out(self):
        """Test that matching moves result in OUT"""
        self.engine.player_batting = True
        is_out, runs, msg = self.engine.play_turn(3, 3)
        
        self.assertTrue(is_out)
        self.assertEqual(runs, 0)
        self.assertIn("OUT", msg)
    
    def test_play_turn_batting(self):
        """Test scoring when player is batting"""
        self.engine.player_batting = True
        is_out, runs, msg = self.engine.play_turn(4, 2)
        
        self.assertFalse(is_out)
        self.assertEqual(runs, 4)
        self.assertEqual(self.engine.player_score, 4)
    
    def test_play_turn_bowling(self):
        """Test scoring when AI is batting"""
        self.engine.player_batting = False
        is_out, runs, msg = self.engine.play_turn(4, 5)
        
        self.assertFalse(is_out)
        self.assertEqual(runs, 5)
        self.assertEqual(self.engine.ai_score, 5)
    
    def test_innings_switch(self):
        """Test innings switching"""
        self.engine.current_innings = 1
        self.engine.player_batting = True
        self.engine.switch_innings()
        
        self.assertEqual(self.engine.current_innings, 2)
        self.assertFalse(self.engine.player_batting)


class TestPlayer(unittest.TestCase):
    """Test Player class"""
    
    def setUp(self):
        self.player = Player("TestPlayer")
    
    def test_make_move(self):
        """Test player can make moves"""
        move = self.player.make_move(3)
        self.assertEqual(move, 3)
        self.assertEqual(len(self.player.move_history), 1)
    
    def test_invalid_move(self):
        """Test invalid moves raise error"""
        with self.assertRaises(ValueError):
            self.player.make_move(0)
        
        with self.assertRaises(ValueError):
            self.player.make_move(7)
    
    def test_move_history(self):
        """Test move history tracking"""
        moves = [1, 2, 3, 4, 5]
        for move in moves:
            self.player.make_move(move)
        
        history = self.player.get_move_history()
        self.assertEqual(history, moves)


class TestStatisticsTracker(unittest.TestCase):
    """Test StatisticsTracker class"""
    
    def setUp(self):
        self.tracker = StatisticsTracker()
    
    def test_add_match(self):
        """Test adding match results"""
        match_data = {
            'player_score': 15,
            'ai_score': 12,
            'winner': 'player'
        }
        self.tracker.add_match(match_data)
        self.assertEqual(len(self.tracker.matches), 1)
    
    def test_win_rate(self):
        """Test win rate calculation"""
        # Add matches with AI winning 2/3
        self.tracker.add_match({'winner': 'ai'})
        self.tracker.add_match({'winner': 'ai'})
        self.tracker.add_match({'winner': 'player'})
        
        ai_win_rate = self.tracker.get_win_rate('ai')
        self.assertAlmostEqual(ai_win_rate, 66.67, places=1)
    
    def test_prediction_accuracy(self):
        """Test prediction accuracy calculation"""
        self.tracker.add_prediction(3, 3, 0.8)  # Correct
        self.tracker.add_prediction(4, 5, 0.6)  # Wrong
        self.tracker.add_prediction(2, 2, 0.9)  # Correct
        
        accuracy = self.tracker.get_prediction_accuracy()
        self.assertAlmostEqual(accuracy, 66.67, places=1)


if __name__ == '__main__':
    unittest.main()
