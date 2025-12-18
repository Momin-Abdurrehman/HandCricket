# Hand Cricket AI - Viva Preparation Guide

**Goal:** This document is designed to help you pass your viva even if you feel like you know nothing right now. Read this twice, and you will be ready.

---

## 1. The "Elevator Pitch" (What is this project?)
**Examiner:** "Tell me about your project."

**You:** 
"This is an AI agent for Hand Cricket that learns to beat human players in real-time. Unlike simple bots that pick random numbers, my agent uses **Pattern Mining** to remember your sequences and **Reinforcement Learning** to adapt to your strategy. It treats the game as a 'Multi-Armed Bandit' problem, balancing between playing winning moves and trying new strategies."

---

## 2. The Algorithms (Explained Simply)

You have implemented two main "brains" for the AI. You need to know what they are called and a simple analogy for each.

### A. N-Gram Models (Pattern Mining)
*   **Where in code:** `src/ai/pattern_mining.py`
*   **The Concept:** Think of **Predictive Text** on your phone. When you type "How are", your phone suggests "you".
*   **How it works here:** If the player plays `3` then `4`, the AI looks at its memory. If in the past, `3` and `4` were usually followed by `6`, the AI predicts `6` is coming next.
*   **Key Term to drop:** "It uses **Markov properties** to predict the next state based on previous states."

### B. UCB1 (Upper Confidence Bound)
*   **Where in code:** `src/ai/predictive_learning.py`
*   **The Concept:** The **Restaurant Problem**.
    *   You have a favorite restaurant (High Reward).
    *   But there is a new restaurant you haven't tried (High Uncertainty).
    *   **Exploitation:** Going to the favorite one (Safe bet).
    *   **Exploration:** Trying the new one (Might be better, might be worse).
*   **How it works here:** The AI picks moves that have won a lot (Exploitation) but occasionally picks moves it hasn't tried in a while (Exploration) to see if they work better now.

### C. FTRL (Follow-The-Regularized-Leader)
*   **Where in code:** `src/ai/predictive_learning.py`
*   **The Concept:** A student taking a quiz.
    *   The student guesses an answer.
    *   The teacher says "Wrong, the answer was B."
    *   The student updates their brain immediately to be closer to "B" for next time.
*   **Key Term to drop:** "It is an **Online Learning** algorithm, meaning it learns incrementally after every single ball, rather than needing a huge dataset beforehand."

---

## 3. Common Viva Questions & Answers

**Q1: Why didn't you use a Neural Network or Deep Learning?**
*   **Answer:** "Neural Networks require thousands of data points to train *before* they work well. This game needs to adapt **instantly** to a specific user. My algorithms (N-grams and Online Learning) start learning from the very first move and adapt much faster in a short game."

**Q2: What is 'Laplace Smoothing' in your code?**
*   **Answer:** "It handles the zero-probability problem. If the player has never played a '6', a standard model would say the probability of '6' is 0%. Smoothing adds a tiny count to everything so the AI acknowledges that a '6' is *possible*, even if it hasn't seen it yet."

**Q3: How does the AI decide what to play?**
*   **Answer:** "It calculates a probability for every possible move (1-6) based on the player's history. Then, it picks the counter-move that beats the most likely player move."

**Q4: What is the time complexity?**
*   **Answer:** "It is very efficient, effectively **O(1)** (constant time) per move, because we use a fixed window size and hash maps (dictionaries) for the N-grams. It doesn't get slower as the game goes on."

---

## 4. Code Structure Cheat Sheet

If they ask you to "Show me the code for X":

*   **"Where is the logic?"** -> Go to `src/ai/` folder.
*   **"Where is the memory?"** -> `src/ai/pattern_mining.py` (Look for `self.ngrams`).
*   **"Where is the learning?"** -> `src/ai/predictive_learning.py` (Look for `update` methods).
*   **"Where is the game loop?"** -> `src/game/engine.py`.

---

## 5. Summary Keywords to Memorize
*   **Stochastic:** Random/Probabilistic (The game isn't deterministic).
*   **Online Learning:** Learning while playing.
*   **Exploration vs. Exploitation:** Trying new things vs. doing what works.
*   **N-gram:** Sequence of N items (e.g., a sequence of 3 moves).
