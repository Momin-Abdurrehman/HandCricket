#!/usr/bin/env python3
"""
Main application for Hand Cricket AI
Provides CLI interface for playing and testing
"""

import sys
import argparse
from src.game import GameEngine, Player, MatchManager, StatisticsTracker
from src.ai import AdaptiveAgent
from src.utils import Visualizer


def play_interactive_game():
    """Play an interactive game against the AI"""
    print("=" * 60)
    print("Welcome to Hand Cricket AI!")
    print("=" * 60)
    print("\nYou will play against an adaptive AI agent that learns")
    print("from your moves and tries to predict your next choice.\n")
    
    # Initialize components
    player = Player("Human Player")
    agent = AdaptiveAgent(use_all_layers=True)
    manager = MatchManager(player, agent)
    
    # Start match
    toss_result = manager.start_new_match()
    print(f"\n{toss_result['message']}")
    print("-" * 60)
    
    turn_count = 0
    
    while True:
        state = manager.get_current_state()
        
        # Display current state
        print(f"\nInnings: {state['current_innings']}")
        print(f"Player Score: {state['player_score']} | AI Score: {state['ai_score']}")
        
        if state['target']:
            print(f"Target: {state['target']}")
        
        if state['player_batting']:
            print("You are BATTING")
        else:
            print("You are BOWLING")
        
        # Get player input
        while True:
            try:
                user_input = input("\nEnter your move (1-6) or 'q' to quit: ").strip()
                
                if user_input.lower() == 'q':
                    print("\nThanks for playing!")
                    return
                
                move = int(user_input)
                if 1 <= move <= 6:
                    break
                else:
                    print("Please enter a number between 1 and 6")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 6")
        
        # Play turn
        result = manager.play_turn(move)
        turn_count += 1
        
        print(f"\nYour move: {result['player_move']} | AI move: {result['ai_move']}")
        print(result['message'])
        
        # Check if innings changed
        if result['innings_complete']:
            print("\n" + "=" * 60)
            print("INNINGS COMPLETE!")
            print("=" * 60)
            input("\nPress Enter to start second innings...")
        
        # Check if game over
        if result['game_over']:
            print("\n" + "=" * 60)
            print("GAME OVER!")
            print("=" * 60)
            print(f"\nFinal Score:")
            print(f"Player: {result['game_state']['player_score']}")
            print(f"AI: {result['game_state']['ai_score']}")
            
            winner = result['winner']
            if winner == 'player':
                print("\n🎉 Congratulations! You WON! 🎉")
            elif winner == 'ai':
                print("\n🤖 AI WINS! Better luck next time! 🤖")
            else:
                print("\n🤝 It's a TIE! 🤝")
            
            # Show AI statistics
            stats = agent.get_statistics()
            print(f"\nAI Prediction Accuracy: {stats['prediction_accuracy']:.1f}%")
            print(f"Total Predictions: {stats['total_predictions']}")
            
            break
    
    # Ask to play again
    play_again = input("\nPlay another game? (y/n): ").strip().lower()
    if play_again == 'y':
        agent.reset()
        play_interactive_game()


def run_simulation(n_matches: int = 10):
    """Run automated simulation for benchmarking"""
    print(f"\nRunning {n_matches} simulated matches...")
    print("=" * 60)
    
    player = Player("Simulated Player")
    agent = AdaptiveAgent(use_all_layers=True)
    manager = MatchManager(player, agent)
    stats_tracker = StatisticsTracker()
    
    for match_num in range(n_matches):
        print(f"\nMatch {match_num + 1}/{n_matches}...", end=" ")
        
        # Start new match
        manager.start_new_match()
        
        # Play until game over
        while True:
            # Simulate player move (random for baseline)
            import random
            player_move = random.randint(1, 6)
            
            result = manager.play_turn(player_move)
            
            # Track predictions
            if len(agent.prediction_history) > 0 and len(agent.move_history) > 0:
                predicted = agent.prediction_history[-1]
                actual = agent.move_history[-1]
                confidence = agent.confidence_scores[-1] if agent.confidence_scores else 0.5
                stats_tracker.add_prediction(actual, predicted, confidence)
            
            if result['game_over']:
                # Record match
                stats_tracker.add_match({
                    'player_score': result['game_state']['player_score'],
                    'ai_score': result['game_state']['ai_score'],
                    'winner': result['winner']
                })
                print(f"Winner: {result['winner'].upper()}")
                break
    
    # Print summary
    print("\n" + "=" * 60)
    print("SIMULATION RESULTS")
    print("=" * 60)
    
    summary = stats_tracker.get_summary()
    print(f"\nTotal Matches: {summary['total_matches']}")
    print(f"AI Win Rate: {summary['ai_win_rate']:.1f}%")
    print(f"Player Win Rate: {summary['player_win_rate']:.1f}%")
    print(f"AI Average Score: {summary['ai_avg_score']:.1f}")
    print(f"Player Average Score: {summary['player_avg_score']:.1f}")
    print(f"AI Prediction Accuracy: {summary['prediction_accuracy']:.1f}%")
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    visualizer = Visualizer()
    
    learning_curve = stats_tracker.get_learning_curve(window_size=20)
    visualizer.plot_learning_curve(learning_curve)
    visualizer.plot_move_frequency(agent.move_history, "AI Observed Move Frequencies")
    visualizer.plot_win_rate_comparison(summary)
    visualizer.plot_score_comparison(summary)
    visualizer.plot_comprehensive_report(agent.move_history, learning_curve, summary)
    
    print("\n✓ Visualizations saved!")


def benchmark_strategies():
    """Benchmark different AI strategies"""
    print("\nBenchmarking AI strategies...")
    print("=" * 60)
    
    strategies = [
        ("Random Baseline", False),
        ("Adaptive AI", True)
    ]
    
    results = {}
    
    for strategy_name, use_all_layers in strategies:
        print(f"\nTesting: {strategy_name}...")
        
        player = Player("Simulated Player")
        agent = AdaptiveAgent(use_all_layers=use_all_layers)
        manager = MatchManager(player, agent)
        stats_tracker = StatisticsTracker()
        
        # Run 20 matches
        for _ in range(20):
            manager.start_new_match()
            
            while True:
                import random
                player_move = random.randint(1, 6)
                result = manager.play_turn(player_move)
                
                if result['game_over']:
                    stats_tracker.add_match({
                        'player_score': result['game_state']['player_score'],
                        'ai_score': result['game_state']['ai_score'],
                        'winner': result['winner']
                    })
                    break
        
        summary = stats_tracker.get_summary()
        results[strategy_name] = summary
        
        print(f"  Win Rate: {summary['ai_win_rate']:.1f}%")
        print(f"  Avg Score: {summary['ai_avg_score']:.1f}")
    
    print("\n" + "=" * 60)
    print("BENCHMARK COMPARISON")
    print("=" * 60)
    
    for strategy_name, summary in results.items():
        print(f"\n{strategy_name}:")
        print(f"  Win Rate: {summary['ai_win_rate']:.1f}%")
        print(f"  Average Score: {summary['ai_avg_score']:.1f}")


def run_gui_mode():
    """Launch the GUI interface"""
    try:
        from src.ui import run as run_gui
        run_gui()
    except ImportError as e:
        if 'tkinter' in str(e).lower() or '_tkinter' in str(e).lower():
            print("=" * 60)
            print("GUI Error: Tkinter is not available")
            print("=" * 60)
            print("\nTkinter is required for the GUI but is not installed in your")
            print("Python environment.")
            print("\nTo fix this on macOS:")
            print("  1. If using system Python: Install python-tk")
            print("     brew install python-tk")
            print("  2. If using pyenv: Reinstall Python with tkinter support")
            print("     pyenv uninstall 3.x.x")
            print("     pyenv install 3.x.x")
            print("  3. Or use the CLI mode instead:")
            print("     python main.py play")
            print("\nAlternatively, you can run the GUI directly if Tkinter is available:")
            print("     python src/ui/gui.py")
            sys.exit(1)
        else:
            rai_modese


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Hand Cricket AI - Adaptive Agent Using Pattern Mining"
    )
    
    parser.add_argument(
        'mode',
        choices=['play', 'simulate', 'benchmark', 'gui'],
        help='Mode: play (interactive CLI), gui (graphical interface), simulate (automated), benchmark (compare strategies)'
    )
    
    parser.add_argument(
        '--matches',
        type=int,
        default=10,
        help='Number of matches for simulation (default: 10)'
    )
    
    args = parser.parse_args()
    
    if args.mode == 'play':
        play_interactive_game()
    elif args.mode == 'gui':
        run_gui_mode()
    elif args.mode == 'simulate':
        run_simulation(args.matches)
    elif args.mode == 'benchmark':
        benchmark_strategies()


if __name__ == "__main__":
    main()
