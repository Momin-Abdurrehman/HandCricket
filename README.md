# Hand Cricket AI

## Adaptive Hand Cricket Agent Using Sequence Modelling and Online Statistical Learning

[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An intelligent, adaptive AI agent for the classic Hand Cricket game that learns from player patterns and adapts its strategy in real-time using advanced pattern mining, predictive learning, and Monte Carlo simulation.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Algorithms & Techniques](#algorithms--techniques)
- [Testing](#testing)
- [Team](#team)
- [License](#license)

---

## 🎯 Overview

Traditional Hand Cricket implementations rely on random number generation or simple heuristics. This project introduces a **fully intelligent adaptive agent** that:

- **Learns** from human player's history
- **Identifies** statistical patterns and habits
- **Predicts** the next move using online sequence modelling
- **Chooses** counter-moves using probabilistic decision engines
- **Adapts** continuously over multiple matches

The agent behaves more like a human opponent, providing a challenging and engaging gameplay experience.

---

## ✨ Features

### Core Game Features
- Complete Hand Cricket game implementation
- Toss system and innings management
- Interactive CLI interface
- Comprehensive statistics tracking
- Match history and replay capabilities

### AI Capabilities
- **Pattern Recognition**: Detects player habits and recurring sequences
- **Online Learning**: Updates predictions in real-time
- **Strategic Decision Making**: Evaluates risk vs reward for each move
- **Adaptive Behavior**: Adjusts strategy based on game situation

### Analysis & Visualization
- Prediction accuracy tracking
- Win rate analysis
- Learning curve visualization
- Move frequency distribution charts
- Comprehensive performance reports

---

## 🏗️ Architecture

The AI agent consists of three computational layers:

### Layer 1: Pattern Mining Layer
Detects frequently recurring patterns using:
- **N-gram Models** (1-gram to 3-gram analysis)
- **Sliding Window Analysis** (frequency distribution)
- **Exponential Moving Average** (recency weighting)
- **Sequential Pattern Detection** (Mini-SPADE style)

### Layer 2: Predictive Learning Layer
Updates predictions online using:
- **FTRL** (Follow-The-Regularized-Leader) - from Google DeepMind research
- **UCB1** (Upper Confidence Bound) - multi-armed bandit algorithm
- **Online Logistic Regression** - incremental weight updates

### Layer 3: Strategic Decision Layer
Makes optimal decisions using:
- **Monte Carlo Simulation** - evaluates thousands of possible outcomes
- **Risk Assessment** - balances scoring potential vs getting out
- **Adaptive Strategy** - changes behavior based on game state

---

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Momin-Abdurrehman/HandCricket.git
cd HandCricket
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Verify installation:
```bash
python -m pytest tests/
```

---

## 🚀 Usage

### Interactive Play Mode
Play against the AI in an interactive session:
```bash
python main.py play
```

### Simulation Mode
Run automated simulations for analysis:
```bash
python main.py simulate --matches 20
```

### Benchmark Mode
Compare different AI strategies:
```bash
python main.py benchmark
```

### Example Demo
Run a quick demonstration:
```bash
python examples/demo_simulation.py
```

---

## 📁 Project Structure

```
HandCricket/
├── src/
│   ├── game/               # Core game engine
│   │   ├── engine.py       # Game rules and flow
│   │   ├── player.py       # Player class
│   │   ├── match_manager.py # Match orchestration
│   │   └── statistics.py   # Stats tracking
│   ├── ai/                 # AI components
│   │   ├── pattern_mining.py    # Layer 1: Pattern detection
│   │   ├── predictive_learning.py # Layer 2: Online learning
│   │   ├── decision_engine.py    # Layer 3: Monte Carlo
│   │   └── agent.py        # Main adaptive agent
│   └── utils/              # Utilities
│       └── visualizer.py   # Visualization tools
├── tests/                  # Unit tests
│   ├── test_game_engine.py
│   └── test_ai_components.py
├── examples/               # Example scripts
│   └── demo_simulation.py
├── main.py                 # Main application
├── requirements.txt        # Dependencies
└── README.md              # This file
```

---

## 🧠 Algorithms & Techniques

### N-gram Sequence Modelling
Analyzes sequences of player moves to detect patterns:
- **Unigrams**: Individual move frequencies
- **Bigrams**: Two-move sequences
- **Trigrams**: Three-move sequences

### FTRL (Follow-The-Regularized-Leader)
Online optimization algorithm used in:
- Google's advertising systems
- DeepMind's reinforcement learning
- Real-time prediction updates

### UCB1 (Upper Confidence Bound)
Multi-armed bandit algorithm that:
- Balances exploration vs exploitation
- Tries new strategies when uncertain
- Converges to optimal actions

### Monte Carlo Simulation
Statistical sampling technique that:
- Simulates thousands of possible outcomes
- Evaluates expected value of each move
- Minimizes risk while maximizing scoring

### Exponential Moving Average
Time-series analysis that:
- Gives more weight to recent moves
- Adapts quickly to behavior changes
- Smooths out noise in predictions

---

## 🧪 Testing

Run all tests:
```bash
python -m pytest tests/ -v
```

Run specific test modules:
```bash
python -m pytest tests/test_game_engine.py -v
python -m pytest tests/test_ai_components.py -v
```

Run individual test files:
```bash
python tests/test_game_engine.py
python tests/test_ai_components.py
```

---

## 📊 Performance Metrics

The system tracks multiple performance indicators:

- **Prediction Accuracy**: % of correctly predicted moves
- **Win Rate**: Percentage of matches won by AI
- **Average Score**: Mean score across all matches
- **Learning Curve**: Accuracy improvement over time
- **Pattern Detection Rate**: Frequency of identified patterns

---

## 🎓 Educational Value

This project demonstrates:

1. **Opponent Modelling**: Techniques used in poker bots and strategy games
2. **Online Learning**: Real-time adaptation without batch training
3. **Pattern Mining**: Extracting meaningful sequences from time-series data
4. **Multi-Armed Bandits**: Balancing exploration and exploitation
5. **Monte Carlo Methods**: Statistical simulation for decision making
6. **Software Engineering**: Clean architecture and testing practices

---

## 👥 Team

**AI Course Project - Fall 2024**

- **Momin Abdurrehman** (502825)
- **Ubaid Sukhera** (501209)
- **Iqra Nisar** (501191)

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🚧 Future Improvements

- [ ] Full GUI with PyGame/Tkinter
- [ ] Cloud-based leaderboard system
- [ ] User profile memory across sessions
- [ ] Deep reinforcement learning agents (PPO, Policy Gradients)
- [ ] Multiplayer online version
- [ ] Adaptive difficulty modes
- [ ] Mobile app version

---

## 📚 References

This project implements algorithms from:

- **N-gram Models**: Natural Language Processing literature
- **FTRL**: McMahan et al., "Ad Click Prediction: a View from the Trenches", KDD 2013
- **UCB1**: Auer et al., "Finite-time Analysis of the Multiarmed Bandit Problem", 2002
- **Monte Carlo Methods**: Metropolis & Ulam, "The Monte Carlo Method", 1949
- **Sequential Pattern Mining**: Zaki, "SPADE: An Efficient Algorithm for Mining Frequent Sequences", 2001

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ for AI Course Project**