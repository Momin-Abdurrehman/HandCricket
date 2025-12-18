"""
Strategic Decision Layer - Layer 3 of the AI system
Implements Monte Carlo simulation for decision making
"""

import numpy as np
from typing import Tuple


class MonteCarloSimulator:
    """
    Monte Carlo sampling engine for evaluating decisions
    Simulates outcomes to minimize risk and maximize scoring
    """
    
    def __init__(self, n_simulations: int = 1000):
        """
        Initialize Monte Carlo simulator
        
        Args:
            n_simulations: Number of simulations per decision
        """
        self.n_simulations = n_simulations
    
    def evaluate_move(self, move: int, opponent_prob_dist: np.ndarray, 
                      is_batting: bool, current_score: int, 
                      opponent_score: int) -> Tuple[float, float]:
        """
        Evaluate a potential move using Monte Carlo simulation
        
        Args:
            move: The move to evaluate (1-6)
            opponent_prob_dist: Probability distribution of opponent's next move
            is_batting: Whether AI is batting
            current_score: AI's current score
            opponent_score: Opponent's current score
        
        Returns:
            Tuple of (expected_value, risk_of_out)
        """
        out_count = 0
        total_runs = 0
        
        for _ in range(self.n_simulations):
            # Sample opponent move from probability distribution
            opponent_move = np.random.choice(range(1, 7), p=opponent_prob_dist)
            
            # Check if out
            if move == opponent_move:
                out_count += 1
            else:
                # Score runs based on who's batting
                if is_batting:
                    total_runs += move
                else:
                    # When bowling, we want to minimize opponent's runs
                    # So we count opponent's runs as negative value
                    total_runs -= opponent_move
        
        risk_of_out = out_count / self.n_simulations
        expected_runs = total_runs / self.n_simulations
        
        return expected_runs, risk_of_out
    
    def choose_best_move(self, opponent_prob_dist: np.ndarray, 
                         is_batting: bool, current_score: int,
                         opponent_score: int, risk_tolerance: float = 0.3) -> int:
        """
        Choose the best move using Monte Carlo evaluation
        
        Args:
            opponent_prob_dist: Probability distribution of opponent's next move
            is_batting: Whether AI is batting
            current_score: AI's current score
            opponent_score: Opponent's current score
            risk_tolerance: Maximum acceptable risk of getting out (0-1)
        
        Returns:
            Best move (1-6)
        """
        best_move = 1
        best_score = float('-inf')
        
        evaluations = []
        
        for move in range(1, 7):
            expected_runs, risk = self.evaluate_move(
                move, opponent_prob_dist, is_batting, current_score, opponent_score
            )
            
            # Calculate utility: balance reward and risk
            # Higher expected runs is good, lower risk is good
            if is_batting:
                # When batting: prioritize runs but avoid getting out
                # Reduced penalty to make AI less overly cautious
                utility = expected_runs - (risk * 6)  # Penalty for risk (reduced from 10)
            else:
                # When bowling: prioritize getting the batsman out
                # Reduced reward to avoid being too aggressive
                utility = (risk * 3) + expected_runs  # Reward risk of opponent getting out (reduced from 5)
            
            evaluations.append({
                'move': move,
                'expected_runs': expected_runs,
                'risk': risk,
                'utility': utility
            })
            
            if utility > best_score:
                best_score = utility
                best_move = move
        
        return best_move
    
    def choose_safe_move(self, opponent_prob_dist: np.ndarray) -> int:
        """
        Choose the safest move (least likely to result in out)
        
        Args:
            opponent_prob_dist: Probability distribution of opponent's next move
        
        Returns:
            Safest move (1-6)
        """
        # Choose the move with lowest predicted probability
        safest_move = int(np.argmin(opponent_prob_dist)) + 1
        return safest_move
    
    def choose_aggressive_move(self, opponent_prob_dist: np.ndarray, 
                               is_batting: bool) -> int:
        """
        Choose an aggressive move (high scoring potential)
        
        Args:
            opponent_prob_dist: Probability distribution of opponent's next move
            is_batting: Whether AI is batting
        
        Returns:
            Aggressive move (1-6)
        """
        if is_batting:
            # When batting, prefer high numbers with acceptable risk
            weights = np.array([1, 2, 3, 4, 5, 6]) * (1 - opponent_prob_dist)
            return int(np.argmax(weights)) + 1
        else:
            # When bowling, try to match opponent's likely moves
            return int(np.argmax(opponent_prob_dist)) + 1
    
    def adaptive_strategy(self, opponent_prob_dist: np.ndarray,
                          is_batting: bool, current_score: int,
                          opponent_score: int, innings: int) -> int:
        """
        Adaptive strategy that changes based on game situation
        
        Args:
            opponent_prob_dist: Probability distribution of opponent's next move
            is_batting: Whether AI is batting
            current_score: AI's current score
            opponent_score: Opponent's current score
            innings: Current innings (1 or 2)
        
        Returns:
            Strategically chosen move
        """
        if innings == 1:
            # First innings: balanced approach with moderate risk
            return self.choose_best_move(
                opponent_prob_dist, is_batting, current_score, opponent_score,
                risk_tolerance=0.30  # Slightly increased from 0.25
            )
        else:
            # Second innings: adapt based on target
            if is_batting:
                target = opponent_score + 1
                runs_needed = target - current_score
                
                if runs_needed <= 0:
                    # Already won, play safe
                    return self.choose_safe_move(opponent_prob_dist)
                elif runs_needed <= 3:
                    # Very close to target, balanced play
                    return self.choose_best_move(
                        opponent_prob_dist, is_batting, current_score, opponent_score,
                        risk_tolerance=0.35
                    )
                elif runs_needed <= 10:
                    # Moderate pressure, slightly aggressive
                    return self.choose_best_move(
                        opponent_prob_dist, is_batting, current_score, opponent_score,
                        risk_tolerance=0.25
                    )
                else:
                    # Need more runs, more aggressive
                    return self.choose_aggressive_move(opponent_prob_dist, is_batting)
            else:
                # Bowling in second innings: defend the score
                runs_ahead = current_score - opponent_score
                
                if runs_ahead <= 3:
                    # Very close game, aggressive bowling
                    return self.choose_aggressive_move(opponent_prob_dist, is_batting)
                elif runs_ahead <= 10:
                    # Moderate lead, balanced approach
                    return self.choose_best_move(
                        opponent_prob_dist, is_batting, current_score, opponent_score,
                        risk_tolerance=0.35
                    )
                else:
                    # Comfortable lead, more conservative
                    return self.choose_best_move(
                        opponent_prob_dist, is_batting, current_score, opponent_score,
                        risk_tolerance=0.40
                    )
