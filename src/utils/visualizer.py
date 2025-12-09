"""
Visualization tools for analyzing agent performance
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Any


class Visualizer:
    """
    Visualization tools for Hand Cricket AI analysis
    """
    
    @staticmethod
    def plot_move_frequency(move_history: List[int], title: str = "Move Frequency Distribution"):
        """
        Plot frequency distribution of moves
        
        Args:
            move_history: List of moves
            title: Plot title
        """
        if not move_history:
            print("No data to plot")
            return
        
        frequencies = [move_history.count(i) for i in range(1, 7)]
        
        plt.figure(figsize=(10, 6))
        plt.bar(range(1, 7), frequencies, color='skyblue', edgecolor='black')
        plt.xlabel('Move (1-6)')
        plt.ylabel('Frequency')
        plt.title(title)
        plt.xticks(range(1, 7))
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('move_frequency.png', dpi=150)
        plt.close()
        print(f"Saved plot: move_frequency.png")
    
    @staticmethod
    def plot_learning_curve(accuracies: List[float], window_size: int = 10):
        """
        Plot prediction accuracy over time
        
        Args:
            accuracies: List of accuracy values
            window_size: Window size for moving average
        """
        if not accuracies:
            print("No accuracy data to plot")
            return
        
        plt.figure(figsize=(12, 6))
        plt.plot(accuracies, alpha=0.6, label='Raw Accuracy')
        
        # Add moving average if enough data
        if len(accuracies) >= window_size:
            moving_avg = []
            for i in range(len(accuracies)):
                start = max(0, i - window_size + 1)
                window = accuracies[start:i+1]
                moving_avg.append(np.mean(window))
            plt.plot(moving_avg, linewidth=2, label=f'Moving Average (window={window_size})')
        
        plt.xlabel('Prediction Number')
        plt.ylabel('Accuracy (%)')
        plt.title('Prediction Accuracy Over Time')
        plt.legend()
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig('learning_curve.png', dpi=150)
        plt.close()
        print(f"Saved plot: learning_curve.png")
    
    @staticmethod
    def plot_win_rate_comparison(stats: Dict[str, Any]):
        """
        Plot win rate comparison
        
        Args:
            stats: Dictionary with statistics
        """
        if 'ai_win_rate' not in stats or 'player_win_rate' not in stats:
            print("Insufficient data for win rate comparison")
            return
        
        categories = ['AI', 'Player']
        win_rates = [stats['ai_win_rate'], stats['player_win_rate']]
        
        plt.figure(figsize=(8, 6))
        bars = plt.bar(categories, win_rates, color=['#2ecc71', '#e74c3c'], edgecolor='black')
        plt.ylabel('Win Rate (%)')
        plt.title('Win Rate Comparison')
        plt.ylim(0, 100)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom')
        
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('win_rate_comparison.png', dpi=150)
        plt.close()
        print(f"Saved plot: win_rate_comparison.png")
    
    @staticmethod
    def plot_score_comparison(stats: Dict[str, Any]):
        """
        Plot average score comparison
        
        Args:
            stats: Dictionary with statistics
        """
        if 'ai_avg_score' not in stats or 'player_avg_score' not in stats:
            print("Insufficient data for score comparison")
            return
        
        categories = ['AI', 'Player']
        scores = [stats['ai_avg_score'], stats['player_avg_score']]
        
        plt.figure(figsize=(8, 6))
        bars = plt.bar(categories, scores, color=['#3498db', '#f39c12'], edgecolor='black')
        plt.ylabel('Average Score')
        plt.title('Average Score Comparison')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom')
        
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('score_comparison.png', dpi=150)
        plt.close()
        print(f"Saved plot: score_comparison.png")
    
    @staticmethod
    def plot_comprehensive_report(move_history: List[int], accuracies: List[float], 
                                   stats: Dict[str, Any]):
        """
        Create a comprehensive visualization report
        
        Args:
            move_history: List of all moves
            accuracies: List of prediction accuracies
            stats: Dictionary with statistics
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Plot 1: Move Frequency
        if move_history:
            frequencies = [move_history.count(i) for i in range(1, 7)]
            axes[0, 0].bar(range(1, 7), frequencies, color='skyblue', edgecolor='black')
            axes[0, 0].set_xlabel('Move (1-6)')
            axes[0, 0].set_ylabel('Frequency')
            axes[0, 0].set_title('Move Frequency Distribution')
            axes[0, 0].set_xticks(range(1, 7))
            axes[0, 0].grid(axis='y', alpha=0.3)
        
        # Plot 2: Learning Curve
        if accuracies:
            axes[0, 1].plot(accuracies, alpha=0.8)
            axes[0, 1].set_xlabel('Prediction Number')
            axes[0, 1].set_ylabel('Accuracy (%)')
            axes[0, 1].set_title('Learning Curve')
            axes[0, 1].grid(alpha=0.3)
        
        # Plot 3: Win Rate
        if 'ai_win_rate' in stats and 'player_win_rate' in stats:
            categories = ['AI', 'Player']
            win_rates = [stats['ai_win_rate'], stats['player_win_rate']]
            bars = axes[1, 0].bar(categories, win_rates, color=['#2ecc71', '#e74c3c'], 
                                 edgecolor='black')
            axes[1, 0].set_ylabel('Win Rate (%)')
            axes[1, 0].set_title('Win Rate Comparison')
            axes[1, 0].set_ylim(0, 100)
            axes[1, 0].grid(axis='y', alpha=0.3)
            
            for bar in bars:
                height = bar.get_height()
                axes[1, 0].text(bar.get_x() + bar.get_width()/2., height,
                              f'{height:.1f}%', ha='center', va='bottom')
        
        # Plot 4: Average Scores
        if 'ai_avg_score' in stats and 'player_avg_score' in stats:
            categories = ['AI', 'Player']
            scores = [stats['ai_avg_score'], stats['player_avg_score']]
            bars = axes[1, 1].bar(categories, scores, color=['#3498db', '#f39c12'], 
                                 edgecolor='black')
            axes[1, 1].set_ylabel('Average Score')
            axes[1, 1].set_title('Average Score Comparison')
            axes[1, 1].grid(axis='y', alpha=0.3)
            
            for bar in bars:
                height = bar.get_height()
                axes[1, 1].text(bar.get_x() + bar.get_width()/2., height,
                              f'{height:.1f}', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('comprehensive_report.png', dpi=150)
        plt.close()
        print(f"Saved comprehensive report: comprehensive_report.png")
