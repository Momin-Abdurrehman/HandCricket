# Quick Start Guide

Get up and running with Hand Cricket AI in 5 minutes!

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Momin-Abdurrehman/HandCricket.git
cd HandCricket
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

That's it! You're ready to go.

## Usage

### Play Interactively

Play a game against the AI:

```bash
python main.py play
```

**What to expect:**
- Choose numbers 1-6 each turn
- AI learns your patterns as you play
- See real-time predictions and statistics
- Complete match with innings and scoring

### Run Simulation

Watch the AI play automated matches:

```bash
python main.py simulate --matches 20
```

**What you get:**
- Automated testing of AI performance
- Statistics and metrics
- Visualization charts saved as PNG files
- Learning curve analysis

### Benchmark Strategies

Compare different AI strategies:

```bash
python main.py benchmark
```

**What it does:**
- Tests random baseline vs adaptive AI
- 20 matches per strategy
- Side-by-side comparison
- Performance metrics

### Interactive Tutorial

Learn how the system works:

```bash
python examples/tutorial.py
```

**What you learn:**
- Game rules and mechanics
- How pattern detection works
- Three-layer AI architecture
- Algorithm explanations
- Try a real game!

### Demo Simulation

Quick demonstration:

```bash
python examples/demo_simulation.py
```

**What it shows:**
- 5 automated matches
- Real-time statistics
- Prediction accuracy
- Win rates

## Understanding the Output

### During Play

```
Innings: 1
Player Score: 12 | AI Score: 0
You are BATTING

Your move (1-6): 4

[AI predicted: 3 (confidence: 0.65)]
Your move: 4 | AI move: 2
Player scores 4 run(s)!
```

**Explanation:**
- AI predicted you'd play 3 with 65% confidence
- You actually played 4
- AI played 2 (trying to get you out)
- Since 4 ≠ 2, you score 4 runs

### After Simulation

```
Total Matches: 10
AI Win Rate: 60.0%
Player Win Rate: 30.0%
AI Average Score: 18.9
Player Average Score: 10.3
AI Prediction Accuracy: 21.1%
```

**What it means:**
- AI won 6/10 matches (60%)
- AI's prediction accuracy improves over time
- AI scores higher on average
- Better than random baseline (~50% win rate)

### Generated Visualizations

After simulation, check these PNG files:

1. **learning_curve.png**: Shows accuracy improving over time
2. **move_frequency.png**: Distribution of moves played
3. **win_rate_comparison.png**: AI vs Player win rates
4. **score_comparison.png**: Average scores
5. **comprehensive_report.png**: All charts combined

## Testing

Run all unit tests:

```bash
python tests/test_game_engine.py
python tests/test_ai_components.py
```

Expected output:
```
............
----------------------------------------------------------------------
Ran 12 tests in 0.000s
OK

.................
----------------------------------------------------------------------
Ran 17 tests in 0.114s
OK
```

## Tips for Playing

### Beat the AI

1. **Vary your moves**: Don't create obvious patterns
2. **Be unpredictable**: Mix up high and low numbers
3. **Change strategies**: Switch patterns mid-game
4. **Use psychology**: AI expects logical patterns

### Watch AI Learn

1. **Try patterns**: Play 3, 3, 3, 3 and watch predictions
2. **Check confidence**: Higher = AI is more sure
3. **See adaptation**: Change pattern and watch adjustment
4. **View statistics**: Track accuracy over turns

## Project Structure

```
HandCricket/
├── main.py              # Main application entry point
├── requirements.txt     # Dependencies
├── README.md           # Full documentation
├── QUICKSTART.md       # This file
├── ARCHITECTURE.md     # System architecture details
├── ALGORITHMS.md       # Algorithm explanations
├── PRESENTATION.md     # Class presentation guide
├── src/
│   ├── game/          # Game engine
│   ├── ai/            # AI algorithms
│   └── utils/         # Visualization tools
├── tests/             # Unit tests
└── examples/          # Demo scripts
```

## Common Issues

### "ModuleNotFoundError: No module named 'numpy'"

**Solution:**
```bash
pip install numpy pandas matplotlib
```

### "Permission denied" when running scripts

**Solution:**
```bash
chmod +x main.py
chmod +x examples/*.py
```

### Plots not displaying

**Solution:**
- PNG files are saved in current directory
- Open them with any image viewer
- Use `ls *.png` to find them

## Next Steps

1. **Read the docs**: Check README.md for detailed information
2. **Explore code**: Look at src/ directory
3. **Try algorithms**: Read ALGORITHMS.md for details
4. **Check architecture**: See ARCHITECTURE.md
5. **Prepare presentation**: Use PRESENTATION.md guide

## Command Reference

| Command | Description |
|---------|-------------|
| `python main.py play` | Play interactively |
| `python main.py simulate` | Run simulation |
| `python main.py simulate --matches N` | Run N matches |
| `python main.py benchmark` | Compare strategies |
| `python examples/tutorial.py` | Interactive tutorial |
| `python examples/demo_simulation.py` | Quick demo |
| `python tests/test_*.py` | Run tests |

## Getting Help

- **Documentation**: Read README.md, ARCHITECTURE.md, ALGORITHMS.md
- **Tutorial**: Run `python examples/tutorial.py`
- **Issues**: Check GitHub issues
- **Code**: All code has docstrings

## Performance Expectations

**Typical Results:**
- AI Win Rate: 55-65% (vs random player)
- Prediction Accuracy: 15-25% (improves with more data)
- Average Game Length: 15-25 turns
- Processing Time: < 1 second per turn

**Factors Affecting Performance:**
- Player predictability (patterns vs random)
- Number of moves (more data = better learning)
- Game state (aggressive vs defensive play)

## Have Fun!

Remember: This is an educational project demonstrating:
- Opponent modelling
- Online learning
- Pattern detection
- Modern AI algorithms

Enjoy exploring the code and playing against the AI! 🎯🏏🤖
