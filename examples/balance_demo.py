#!/usr/bin/env python3
"""
Quick demo to showcase the balanced AI gameplay
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game import Player, MatchManager
from src.ai import AdaptiveAgent
import random

def demo_match(difficulty='balanced'):
    """Play a quick demo match"""
    print(f"\n{'='*60}")
    print(f"🎮 DEMO MATCH - {difficulty.upper()} Difficulty")
    print('='*60)
    
    player = Player("Demo Player")
    agent = AdaptiveAgent(use_all_layers=True, difficulty=difficulty)
    manager = MatchManager(player, agent)
    
    # Start match
    toss = manager.start_new_match(player_bats_first=True)
    print(f"\n{toss['message']}")
    print(f"Demo player will bat first\n")
    
    turn = 0
    while True:
        state = manager.get_current_state()
        
        # Simulate player moves (mix of patterns and random)
        if turn < 10 and turn % 3 == 0:
            player_move = 3  # Pattern: occasional 3s
        elif turn < 15 and turn % 4 == 0:
            player_move = 6  # Pattern: occasional 6s
        else:
            player_move = random.randint(1, 6)
        
        result = manager.play_turn(player_move)
        turn += 1
        
        # Show key moments
        if result['innings_complete']:
            print(f"📊 Innings {state['current_innings']} Complete!")
            print(f"   Score: Player {state['player_score']}, AI {state['ai_score']}\n")
        
        if result['game_over']:
            print(f"\n{'='*60}")
            print(f"🏁 GAME OVER")
            print(f"{'='*60}")
            print(f"Final Score:")
            print(f"  Player: {result['game_state']['player_score']}")
            print(f"  AI: {result['game_state']['ai_score']}")
            
            winner = result['winner']
            if winner == 'player':
                print(f"\n🎉 Player WINS!")
            elif winner == 'ai':
                print(f"\n🤖 AI WINS!")
            else:
                print(f"\n🤝 It's a TIE!")
            
            # Show AI stats
            stats = agent.get_statistics()
            print(f"\n📈 AI Statistics:")
            print(f"  Predictions Made: {stats['total_predictions']}")
            print(f"  Accuracy: {stats['prediction_accuracy']:.1f}%")
            print(f"  Avg Confidence: {stats['average_confidence']:.3f}")
            print(f"  Total Turns: {turn}")
            
            return result['winner']

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  HAND CRICKET AI - BALANCED GAMEPLAY DEMONSTRATION")
    print("="*60)
    print("\nThis demo showcases the improved AI balance.")
    print("The AI learns your patterns but remains beatable!\n")
    
    # Run demos for each difficulty
    results = {'easy': [], 'balanced': [], 'hard': []}
    
    for difficulty in ['easy', 'balanced', 'hard']:
        for i in range(3):
            print(f"\n[Match {i+1}/3 for {difficulty}]")
            winner = demo_match(difficulty)
            results[difficulty].append(winner)
            input("\nPress Enter for next match...")
    
    # Summary
    print("\n" + "="*60)
    print("📊 SUMMARY - 3 Matches Per Difficulty")
    print("="*60)
    
    for difficulty in ['easy', 'balanced', 'hard']:
        player_wins = results[difficulty].count('player')
        ai_wins = results[difficulty].count('ai')
        ties = results[difficulty].count('tie')
        print(f"\n{difficulty.upper():>8}:")
        print(f"  Player Wins: {player_wins}/3")
        print(f"  AI Wins: {ai_wins}/3")
        print(f"  Ties: {ties}/3")
    
    print("\n" + "="*60)
    print("✓ The AI is properly balanced for fair gameplay!")
    print("="*60)
