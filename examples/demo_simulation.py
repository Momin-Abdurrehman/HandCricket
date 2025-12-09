#!/usr/bin/env python3
"""
Demo script showing automated simulation
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game import Player, MatchManager, StatisticsTracker
from src.ai import AdaptiveAgent
import random


def main():
    print("=" * 60)
    print("Hand Cricket AI - Simulation Demo")
    print("=" * 60)
    
    # Initialize components
    player = Player("Demo Player")
    agent = AdaptiveAgent(use_all_layers=True)
    manager = MatchManager(player, agent)
    stats_tracker = StatisticsTracker()
    
    n_matches = 5
    print(f"\nRunning {n_matches} demonstration matches...\n")
    
    for match_num in range(n_matches):
        print(f"Match {match_num + 1}:")
        print("-" * 40)
        
        # Start match
        manager.start_new_match()
        turn_count = 0
        
        # Play until game over
        while True:
            # Simulate player move (random for demo)
            player_move = random.randint(1, 6)
            result = manager.play_turn(player_move)
            turn_count += 1
            
            # Track predictions
            if len(agent.prediction_history) > 0 and len(agent.move_history) > 0:
                predicted = agent.prediction_history[-1]
                actual = agent.move_history[-1]
                confidence = agent.confidence_scores[-1] if agent.confidence_scores else 0.5
                stats_tracker.add_prediction(actual, predicted, confidence)
            
            if result['game_over']:
                stats_tracker.add_match({
                    'player_score': result['game_state']['player_score'],
                    'ai_score': result['game_state']['ai_score'],
                    'winner': result['winner']
                })
                
                print(f"Final Score - Player: {result['game_state']['player_score']}, "
                      f"AI: {result['game_state']['ai_score']}")
                print(f"Winner: {result['winner'].upper()}")
                print(f"Total turns: {turn_count}")
                print()
                break
    
    # Print summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    summary = stats_tracker.get_summary()
    print(f"\nTotal Matches: {summary['total_matches']}")
    print(f"AI Win Rate: {summary['ai_win_rate']:.1f}%")
    print(f"Player Win Rate: {summary['player_win_rate']:.1f}%")
    print(f"AI Average Score: {summary['ai_avg_score']:.1f}")
    print(f"Player Average Score: {summary['player_avg_score']:.1f}")
    print(f"AI Prediction Accuracy: {summary['prediction_accuracy']:.1f}%")
    
    # Show agent statistics
    agent_stats = agent.get_statistics()
    print(f"\nAgent Statistics:")
    print(f"Total Predictions: {agent_stats['total_predictions']}")
    print(f"Prediction Accuracy: {agent_stats['prediction_accuracy']:.1f}%")
    print(f"Average Confidence: {agent_stats['average_confidence']:.3f}")


if __name__ == "__main__":
    main()
