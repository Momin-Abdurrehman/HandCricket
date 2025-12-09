# Algorithm Details

This document provides detailed explanations of all algorithms used in the Hand Cricket AI system.

## Table of Contents

1. [Pattern Mining Algorithms](#pattern-mining-algorithms)
2. [Predictive Learning Algorithms](#predictive-learning-algorithms)
3. [Decision Making Algorithms](#decision-making-algorithms)
4. [Why These Algorithms?](#why-these-algorithms)

---

## Pattern Mining Algorithms

### 1. N-gram Sequence Model

**What is it?**
N-grams are contiguous sequences of N items from a given sample. In our case, sequences of N moves.

**How it works:**
```
Unigram (N=1):  [3] → counts individual moves
Bigram (N=2):   [3, 4] → counts two-move sequences
Trigram (N=3):  [3, 4, 6] → counts three-move sequences
```

**Example:**
```
Player history: [1, 2, 3, 2, 3, 4]

Bigram counts:
(1, 2): 1
(2, 3): 2  ← appears twice!
(3, 2): 1
(3, 4): 1

Prediction after seeing [2]:
P(next=3) = 2/3 = 0.67  ← High probability!
P(next=4) = 1/3 = 0.33
```

**Mathematical Formula:**
```
P(move_i | move_{i-1}, ..., move_{i-n+1}) = 
    Count(move_{i-n+1}, ..., move_i) / 
    Count(move_{i-n+1}, ..., move_{i-1})
```

**Why use it?**
- Captures sequential dependencies
- Used in natural language processing
- Effective for pattern recognition
- Simple yet powerful

**Origin:**
Natural Language Processing, Google's language models

---

### 2. Sliding Window Analysis

**What is it?**
Maintains a fixed-size window of the most recent moves and analyzes their frequency.

**How it works:**
```
Window size = 5
Player moves: [1, 2, 3, 4, 5, 6, 1, 2, 3]
                          └─────────┘
                          Current window: [6, 1, 2, 3]

Frequency: {1: 20%, 2: 20%, 3: 20%, 6: 20%, others: 5%}
```

**Mathematical Formula:**
```
P(move_i) = Count(move_i in window) / window_size
```

**Cycle Detection:**
```
History: [1, 2, 3, 1, 2, 3, 1, 2, 3]
                 └─────┘ 
         Pattern [1, 2, 3] repeats 3 times!
```

**Why use it?**
- Captures recent behavior
- Adapts quickly to changes
- Detects cyclic patterns
- Simple and efficient

**Origin:**
Time series analysis, signal processing

---

### 3. Exponential Moving Average (EMA)

**What is it?**
A weighted average that gives exponentially decreasing weights to older observations.

**How it works:**
```
α = 0.3 (smoothing factor)

Move 1: [3] → EMA = [0, 0, 1, 0, 0, 0] * 0.3 + previous * 0.7
Move 2: [3] → EMA = [0, 0, 1, 0, 0, 0] * 0.3 + EMA * 0.7
Move 3: [4] → EMA = [0, 0, 0, 1, 0, 0] * 0.3 + EMA * 0.7
```

**Mathematical Formula:**
```
EMA_t = α * observation_t + (1 - α) * EMA_{t-1}

where:
- α ∈ [0, 1] is the smoothing factor
- Higher α gives more weight to recent data
```

**Why use it?**
- Reacts quickly to changes
- Smooth predictions
- Used in stock market analysis
- Exponentially decaying memory

**Origin:**
Financial time series analysis, control systems

---

### 4. Sequential Pattern Mining (SPADE-style)

**What is it?**
Discovers frequently occurring subsequences in a sequence database.

**How it works:**
```
Player history: [1, 2, 3, 1, 2, 3, 4, 1, 2]

Frequent patterns (min_support = 2):
[1, 2]: appears 3 times
[1, 2, 3]: appears 2 times
[2, 3]: appears 2 times

If last moves are [1, 2], predict: 3 (continues pattern)
```

**Algorithm:**
```
1. Find all frequent 1-sequences
2. For each frequent k-sequence:
   a. Generate (k+1)-candidates
   b. Count occurrences
   c. Keep if frequency ≥ min_support
3. Repeat until no more frequent patterns
```

**Why use it?**
- Discovers hidden patterns
- Used in market basket analysis
- Finds non-obvious sequences
- Robust to noise

**Origin:**
Zaki's SPADE algorithm (Sequential Pattern Discovery using Equivalence classes), 2001

---

## Predictive Learning Algorithms

### 5. FTRL (Follow-The-Regularized-Leader)

**What is it?**
An online learning algorithm that updates predictions based on observed errors with regularization.

**How it works:**
```
1. Make prediction with current weights
2. Observe actual outcome
3. Calculate loss (error)
4. Update weights to minimize cumulative loss + regularization
```

**Mathematical Formula:**
```
At each step t:

1. Predict: w_t = argmin_w (sum_{s=1}^{t-1} g_s · w + λ₁|w| + λ₂w²)

2. Observe: actual outcome

3. Update: g_t = gradient of loss

where:
- g_s: accumulated gradients
- λ₁: L1 regularization (sparsity)
- λ₂: L2 regularization (smoothness)
```

**Example:**
```
Predicted: move 3 (probability 0.6)
Actual: move 4
Loss: 1.0 (wrong prediction)

Weight update:
w[3] decreases (was wrong)
w[4] increases (should predict this)
```

**Why use it?**
- Used by Google for ad click prediction
- Handles millions of features
- Online updates (no batch training)
- Regularization prevents overfitting

**Origin:**
McMahan et al., "Ad Click Prediction: a View from the Trenches", KDD 2013

---

### 6. UCB1 (Upper Confidence Bound)

**What is it?**
A multi-armed bandit algorithm that balances trying new actions (exploration) vs using best known action (exploitation).

**How it works:**
```
Each move is an "arm" of a slot machine.
Choose arm with highest UCB score:

UCB(move_i) = average_reward(move_i) + c * sqrt(ln(total_pulls) / pulls(move_i))
                  └─ exploitation ─┘     └────── exploration ──────┘
```

**Mathematical Formula:**
```
UCB_i = Q̄_i + c * sqrt(ln(N) / n_i)

where:
- Q̄_i: average reward for action i
- N: total number of actions taken
- n_i: number of times action i was taken
- c: exploration parameter (typically √2)
```

**Example:**
```
Move statistics after 100 turns:
Move 1: pulled 30 times, avg reward: 0.7
Move 2: pulled 10 times, avg reward: 0.6
Move 3: pulled 5 times, avg reward: 0.5

UCB scores:
Move 1: 0.7 + 2*sqrt(ln(45)/30) = 0.87
Move 2: 0.6 + 2*sqrt(ln(45)/10) = 1.32 ← highest!
Move 3: 0.5 + 2*sqrt(ln(45)/5) = 1.75 ← unexplored bonus

Choose Move 3 (exploration) or Move 1 (exploitation) depending on c
```

**Why use it?**
- Provably optimal regret bounds
- Automatic exploration-exploitation balance
- Used in clinical trials, A/B testing
- Simple and effective

**Origin:**
Auer, Cesa-Bianchi, Fischer, "Finite-time Analysis of the Multiarmed Bandit Problem", 2002

---

### 7. Online Logistic Regression

**What is it?**
Multi-class classification that updates weights incrementally with each new example.

**How it works:**
```
1. Extract features from recent move history
2. Compute logits: z = W·x + b
3. Apply softmax: P(class_i) = exp(z_i) / sum(exp(z_j))
4. Observe true class
5. Update weights: W ← W - α·∇L
```

**Mathematical Formula:**
```
Forward pass:
P(y=k|x) = exp(w_k·x + b_k) / Σ_j exp(w_j·x + b_j)

Gradient:
∇w_k = x · (P(y=k|x) - y_k)

Update:
w_k ← w_k - α · ∇w_k
```

**Feature Extraction:**
```
Recent moves: [1, 2, 3, 4, 5]
Features: [1/6, 2/6, 3/6, 4/6, 5/6]  ← normalized
```

**Why use it?**
- Standard ML classification
- Online learning variant
- Probabilistic outputs
- Interpretable weights

**Origin:**
Online learning literature, follows standard stochastic gradient descent

---

## Decision Making Algorithms

### 8. Monte Carlo Simulation

**What is it?**
Statistical simulation that uses random sampling to estimate outcomes.

**How it works:**
```
To evaluate move M:

For i = 1 to N simulations:
    1. Sample opponent's move from probability distribution
    2. Check if M == opponent_move (OUT?)
    3. Calculate runs scored
    4. Accumulate results

Expected value = total_runs / N
Risk = count_outs / N
```

**Example:**
```
Evaluating move 3, opponent distribution: [0.1, 0.2, 0.3, 0.2, 0.1, 0.1]

Run 1000 simulations:
- Opponent played 3: 300 times → OUT
- Opponent played other: 700 times → scored 3 runs each

Expected runs: (700 * 3) / 1000 = 2.1
Risk: 300 / 1000 = 0.30

Utility: 2.1 - penalty * 0.30
```

**Utility Function:**
```
When batting:
U(move) = Expected_Runs - 10 * Risk_of_Out

When bowling:
U(move) = 5 * Risk_of_Out - Expected_Opponent_Runs
```

**Why use it?**
- Handles uncertainty naturally
- Used in physics, finance, AI
- Doesn't require analytical solution
- Accurate with enough samples

**Origin:**
Metropolis & Ulam, "The Monte Carlo Method", 1949
Used in AlphaGo, poker bots, etc.

---

### 9. Adaptive Strategy

**What is it?**
Changes decision strategy based on game state.

**How it works:**
```
First Innings:
→ Balanced approach
→ Moderate risk tolerance

Second Innings (batting):
If far from target:
    → Aggressive (take risks)
If close to target:
    → Safe (minimize outs)
If winning:
    → Very safe

Second Innings (bowling):
If small lead:
    → Aggressive (get them out)
If large lead:
    → Balanced
```

**Decision Tree:**
```
Is second innings?
├─ No → Balanced strategy
└─ Yes
   ├─ Batting?
   │  ├─ Need > 10 runs → Aggressive
   │  ├─ Need 5-10 runs → Balanced
   │  └─ Need < 5 runs → Safe
   └─ Bowling?
      ├─ Lead < 5 → Aggressive (go for out)
      └─ Lead ≥ 5 → Balanced
```

**Why use it?**
- Mimics human strategic thinking
- Context-aware decisions
- Maximizes win probability
- Realistic gameplay

---

## Why These Algorithms?

### Design Philosophy

1. **Non-Syllabus Requirement**
   - None of these were taught in the AI course
   - All come from modern research and industry

2. **Complementary Strengths**
   - N-grams: Sequential patterns
   - Sliding window: Recent trends
   - EMA: Smooth adaptation
   - FTRL: Online optimization
   - UCB1: Exploration/exploitation
   - Monte Carlo: Decision under uncertainty

3. **Real-World Applications**
   - Used in Google (FTRL, n-grams)
   - Used in DeepMind (UCB1, Monte Carlo)
   - Used in finance (EMA)
   - Used in data mining (SPADE)

4. **Opponent Modelling**
   - All algorithms contribute to understanding player behavior
   - Layer 1: What patterns exist?
   - Layer 2: How confident are we?
   - Layer 3: What should we do?

### Performance Characteristics

| Algorithm | Time Complexity | Space Complexity | Adaptation Speed |
|-----------|----------------|------------------|------------------|
| N-gram | O(n) | O(6^n) | Slow |
| Sliding Window | O(1) | O(w) | Fast |
| EMA | O(1) | O(1) | Medium |
| SPADE | O(p) | O(p) | Slow |
| FTRL | O(k) | O(k) | Fast |
| UCB1 | O(k) | O(k) | Medium |
| Online LR | O(k*f) | O(k*f) | Fast |
| Monte Carlo | O(n*k) | O(1) | N/A |

Where:
- n: n-gram length
- w: window size
- p: number of patterns
- k: number of actions
- f: number of features

### Comparison with Course Algorithms

**Why not Minimax?**
- Assumes perfect information
- Assumes adversarial opponent
- Doesn't model player habits
- Can't adapt to patterns

**Why not Expectiminimax?**
- Assumes fixed probability distribution
- Doesn't learn from history
- Can't detect patterns
- Static strategy

**Why not Bayesian Networks?**
- Requires predefined structure
- Hard to define dependencies
- Doesn't capture temporal patterns
- Complex inference

**Why not Hidden Markov Models?**
- Fixed state space
- Assumes Markov property
- Doesn't capture long-term patterns
- Training complexity

**Why not MDPs?**
- Requires reward function design
- Large state space
- Doesn't model opponent
- Complex value iteration

### Advantages of Our Approach

1. **Learns Online**: Updates with each move, no batch training
2. **Adapts Quickly**: Responds to behavior changes
3. **Probabilistic**: Handles uncertainty naturally
4. **Interpretable**: Can explain predictions
5. **Scalable**: Efficient computation
6. **Robust**: Handles noisy data
7. **Modern**: Used in real AI systems

---

## Further Reading

### N-grams
- Jurafsky & Martin, "Speech and Language Processing"
- Google N-gram Viewer

### FTRL
- McMahan et al., "Ad Click Prediction: a View from the Trenches", KDD 2013
- Google Research Blog

### UCB1
- Auer et al., "Finite-time Analysis of the Multiarmed Bandit Problem", Machine Learning 2002
- Sutton & Barto, "Reinforcement Learning: An Introduction"

### Monte Carlo Methods
- Metropolis & Ulam, "The Monte Carlo Method", 1949
- Silver et al., "Mastering the game of Go with deep neural networks and tree search", Nature 2016

### Sequential Pattern Mining
- Zaki, "SPADE: An Efficient Algorithm for Mining Frequent Sequences", Machine Learning 2001

### Online Learning
- Hazan, "Introduction to Online Convex Optimization", 2016
- Shalev-Shwartz, "Online Learning and Online Convex Optimization", 2011
