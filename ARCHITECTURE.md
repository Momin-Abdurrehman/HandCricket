# Architecture Documentation

## System Architecture

The Hand Cricket AI system follows a modular, three-layer architecture that separates concerns and enables easy testing and extension.

## High-Level Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Main Application                      │
│                      (main.py)                           │
└───────────────────┬─────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌───────────────┐      ┌────────────────┐
│  Game Engine  │      │   AI Agent     │
│               │◄─────┤                │
└───────────────┘      └────────────────┘
        │                       │
        │                       │
        ▼                       ▼
┌───────────────┐      ┌────────────────┐
│  Statistics   │      │ Visualization  │
│    Tracker    │      │     Tools      │
└───────────────┘      └────────────────┘
```

## Component Details

### 1. Game Engine Layer (`src/game/`)

#### GameEngine (`engine.py`)
- **Purpose**: Implements core game rules and mechanics
- **Responsibilities**:
  - Validate moves (1-6)
  - Process turns (batting/bowling)
  - Detect outs (matching moves)
  - Track scores and innings
  - Determine game completion and winner

#### Player (`player.py`)
- **Purpose**: Represents a human player
- **Responsibilities**:
  - Record move history
  - Validate player inputs
  - Provide move history for AI analysis

#### MatchManager (`match_manager.py`)
- **Purpose**: Orchestrates complete matches
- **Responsibilities**:
  - Coordinate player and AI interactions
  - Manage match flow and state
  - Handle toss and innings transitions
  - Record match results

#### StatisticsTracker (`statistics.py`)
- **Purpose**: Track performance metrics
- **Responsibilities**:
  - Calculate win rates
  - Track prediction accuracy
  - Compute average scores
  - Generate learning curves

### 2. AI Agent Layer (`src/ai/`)

The AI is organized into three computational layers:

#### Layer 1: Pattern Mining (`pattern_mining.py`)

##### NGramModel
- Analyzes sequences of length 1-3
- Builds conditional probability tables
- Predicts next move based on recent history
- Uses Laplace smoothing for unseen sequences

##### SlidingWindowAnalyzer
- Maintains fixed-size window of recent moves
- Computes frequency distribution
- Detects cyclic patterns
- Adapts quickly to behavior changes

##### ExponentialMovingAverage
- Applies exponential weighting to moves
- Gives higher weight to recent observations
- Smooths out noise in predictions
- Converges quickly to current behavior

##### SequentialPatternDetector
- Finds frequent subsequences (SPADE-style)
- Matches patterns in player history
- Identifies recurring sequences
- Predicts continuations of patterns

#### Layer 2: Predictive Learning (`predictive_learning.py`)

##### FTRLOptimizer
- Follow-The-Regularized-Leader algorithm
- Updates weights based on prediction errors
- Uses L1/L2 regularization
- Converges to optimal weights over time

##### UCB1
- Upper Confidence Bound bandit algorithm
- Balances exploration vs exploitation
- Tries uncertain actions with bonus
- Converges to best actions

##### OnlineLogisticRegression
- Multi-class classification
- Incremental weight updates
- Feature extraction from move history
- Softmax probability output

#### Layer 3: Strategic Decision (`decision_engine.py`)

##### MonteCarloSimulator
- Simulates thousands of possible outcomes
- Evaluates expected value of each move
- Assesses risk of getting out
- Balances scoring potential vs safety

##### Decision Strategies
- **Safe Strategy**: Minimize risk of out
- **Aggressive Strategy**: Maximize scoring
- **Balanced Strategy**: Optimize utility function
- **Adaptive Strategy**: Changes based on game state

#### AdaptiveAgent (`agent.py`)

Main agent that integrates all three layers:

```
Player Move
     │
     ▼
┌─────────────────────────────────────┐
│   Layer 1: Pattern Mining            │
│   - N-grams                          │
│   - Sliding Window                   │
│   - EMA                              │
│   - Sequential Patterns              │
└──────────────┬──────────────────────┘
               │
               ▼
        Probability Distribution
               │
               ▼
┌─────────────────────────────────────┐
│   Layer 2: Predictive Learning      │
│   - FTRL                             │
│   - UCB1                             │
│   - Online LR                        │
└──────────────┬──────────────────────┘
               │
               ▼
        Refined Predictions
               │
               ▼
┌─────────────────────────────────────┐
│   Layer 3: Strategic Decision       │
│   - Monte Carlo Simulation          │
│   - Risk Assessment                 │
│   - Adaptive Strategy               │
└──────────────┬──────────────────────┘
               │
               ▼
          AI Move (1-6)
```

### 3. Utilities Layer (`src/utils/`)

#### Visualizer (`visualizer.py`)
- **Purpose**: Generate analytical visualizations
- **Capabilities**:
  - Move frequency histograms
  - Learning curve plots
  - Win rate comparisons
  - Score comparisons
  - Comprehensive reports

## Data Flow

### During a Turn

1. **User Input**: Player enters move (1-6)
2. **Player Processing**: MatchManager receives and validates move
3. **AI Processing**:
   - Agent receives player history
   - Layer 1 analyzes patterns
   - Layer 2 refines predictions
   - Layer 3 selects optimal move
4. **Game Processing**: GameEngine processes both moves
5. **Result**: Determines if out, calculates runs
6. **Update**: Agent updates internal models
7. **Statistics**: Tracker records prediction accuracy

### Learning Loop

```
Player Move → Pattern Detection → Prediction → Decision → Outcome
                                                              │
                                                              ▼
                                                    Model Update
                                                              │
                                                              └─→ Improved Predictions
```

## Algorithm Integration

### Probability Aggregation

The agent combines predictions from multiple sources:

```python
P_final = 0.20 * P_ngram +      # Historical patterns
          0.15 * P_window +      # Recent frequency
          0.20 * P_ema +         # Weighted recent
          0.15 * P_patterns +    # Sequential patterns
          0.15 * P_ftrl +        # FTRL learning
          0.10 * P_ucb1 +        # UCB1 exploration
          0.05 * P_lr            # Logistic regression
```

Weights can be adjusted for different behavior profiles.

### Decision Making

Given probability distribution P over opponent's next move:

1. **Evaluate each possible move (1-6)**:
   ```
   For each move m:
     Simulate N times:
       Sample opponent_move from P
       If m == opponent_move: count_out++
       Else: accumulate_runs += score(m)
     
     risk[m] = count_out / N
     expected_runs[m] = accumulate_runs / N
     utility[m] = expected_runs[m] - risk_penalty * risk[m]
   ```

2. **Select move with highest utility**

### Online Learning

After each turn:

1. **Update Pattern Mining**:
   - Add move to n-gram counts
   - Update sliding window
   - Update EMA with new observation
   - Add to sequential pattern database

2. **Update Predictive Learning**:
   - Calculate prediction error
   - Update FTRL weights
   - Update UCB1 statistics
   - Train online logistic regression

3. **Accumulate Statistics**:
   - Record prediction accuracy
   - Update learning curve
   - Track pattern frequencies

## Extensibility Points

### Adding New Pattern Detectors

1. Create class in `pattern_mining.py`
2. Implement `predict_probabilities()` method
3. Add to `AdaptiveAgent._aggregate_pattern_predictions()`
4. Adjust weight in probability combination

### Adding New Learning Algorithms

1. Create class in `predictive_learning.py`
2. Implement `update()` and `get_probabilities()` methods
3. Initialize in `AdaptiveAgent.__init__()`
4. Add to aggregation function

### Adding New Decision Strategies

1. Add method to `MonteCarloSimulator`
2. Implement custom utility function
3. Call from `AdaptiveAgent.choose_move()`

## Performance Considerations

### Computational Complexity

- **N-gram update**: O(n) where n is max n-gram length
- **Monte Carlo evaluation**: O(k * m) where k = simulations, m = moves
- **Pattern detection**: O(w * p) where w = window size, p = pattern length
- **Total per turn**: O(n + k*m + w*p) ≈ O(k*m) dominated by MC simulation

### Memory Usage

- **N-gram storage**: O(6^n) worst case, typically sparse
- **Move history**: O(t) where t = total turns
- **Pattern database**: O(p * f) where p = unique patterns, f = frequency
- **Total**: Linear in number of turns, manageable for typical games

### Optimization Opportunities

1. **Reduce MC simulations** for non-critical situations
2. **Limit n-gram depth** based on available data
3. **Prune infrequent patterns** to save memory
4. **Cache probability calculations** within same turn

## Testing Strategy

### Unit Tests

- **Game Engine**: Test rules, scoring, state transitions
- **Pattern Mining**: Verify pattern detection and prediction
- **Learning Algorithms**: Check convergence and updates
- **Decision Engine**: Validate utility calculations

### Integration Tests

- **Full Matches**: Simulate complete games
- **Learning Verification**: Check accuracy improves over time
- **Strategy Comparison**: Benchmark different approaches

### Validation

- **Prediction Accuracy**: Should improve with more data
- **Win Rate**: AI should win > 50% vs random player
- **Pattern Detection**: Should identify obvious patterns
- **Adaptation**: Should adjust to behavior changes

## Configuration

### Tunable Parameters

#### Pattern Mining
- `n`: N-gram length (default: 3)
- `window_size`: Sliding window size (default: 20)
- `alpha`: EMA smoothing factor (default: 0.3)
- `min_support`: Pattern minimum support (default: 2)

#### Predictive Learning
- `learning_rate`: FTRL/LR learning rate (default: 0.01-0.1)
- `lambda1`, `lambda2`: FTRL regularization (default: 0.1, 1.0)
- `c`: UCB1 exploration constant (default: 2.0)

#### Decision Making
- `n_simulations`: Monte Carlo samples (default: 1000)
- `risk_tolerance`: Risk acceptance level (default: 0.3)

#### Aggregation
- Probability combination weights (sum to 1.0)

## Deployment

### Requirements
- Python 3.10+
- NumPy for numerical operations
- Pandas for data management
- Matplotlib for visualization

### Scalability
- Can handle thousands of moves per session
- Memory usage scales linearly with game length
- CPU usage dominated by Monte Carlo simulation
- Can be optimized with multiprocessing

### Production Considerations
- Save/load agent state for persistence
- Log all predictions for offline analysis
- Monitor prediction accuracy in real-time
- A/B test different parameter configurations
