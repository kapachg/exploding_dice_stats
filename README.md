# Exploding Dice Probability Analysis

## 📊 Project Overview

This project provides comprehensive mathematical analysis and visualization of **exploding dice mechanics**, including both single-die and two-dice (maximum) variants.

## 🎲 What Are Exploding Dice?

An exploding die is a fair die where:
1. Each face (1 to n) has equal probability
2. Rolling the maximum value (n) triggers a "re-roll and add" mechanic
3. This process repeats indefinitely as long as the maximum continues to appear
4. Standard notation: dX (e.g., d6 = six-sided die)

## 📁 Project Files

### Analysis Reports
- **`EXPLODING_DICE_ANALYSIS.md`** - Complete analysis of single exploding dice
- **`TWO_DICE_ANALYSIS.md`** - Analysis of maximum-of-two-dice mechanic

### Code
- **`exploding_dice.py`** - Python implementation with exact probability calculations

### Visualizations
#### Single Die Analysis:
- **`exploding_dice_probabilities.png`** - Bar chart + line plot
- **`exploding_dice_heatmap.png`** - Probability heatmap

#### Two Dice Analysis:
- **`two_dice_probabilities.png`** - Triple-panel visualization (bars + lines + marginal improvements)
- **`two_dice_heatmap.png`** - Probability heatmap for dice pairings

## 🎯 Quick Results

### Part 1: Single Exploding Die

**Probability of reaching at least target value:**

| Die   | ≥4     | ≥6     | ≥8     | ≥10    |
|-------|--------|--------|--------|--------|
| d4    | 25.0%  | 18.8%  | 6.3%   | 4.7%   |
| d6    | 50.0%  | 16.7%  | 13.9%  | 8.3%   |
| d8    | 62.5%  | 37.5%  | 12.5%  | 10.9%  |
| d10   | 70.0%  | 50.0%  | 30.0%  | 10.0%  |
| d12   | 75.0%  | 58.3%  | 41.7%  | 25.0%  |

**Key Insight**: Larger dice have higher probabilities despite exploding less frequently!

### Part 2: Two Dice (Maximum of d6 + dX)

**Probability that max(d6, dX) reaches at least target:**

| Dice Pair | ≥4     | ≥6     | ≥8     | ≥10    |
|-----------|--------|--------|--------|--------|
| d6+d4     | 62.5%  | 32.3%  | 19.3%  | 12.6%  |
| d6+d6     | 75.0%  | 30.6%  | 25.9%  | 16.0%  |
| d6+d8     | 81.3%  | 47.9%  | 24.7%  | 18.4%  |
| d6+d10    | 85.0%  | 58.3%  | 39.7%  | 17.5%  |
| d6+d12    | 87.5%  | 65.3%  | 49.8%  | 31.3%  |

**Key Insight**: Two dice dramatically improve success rates (nearly double for many targets)!

## 💡 Major Findings

### Single Die Insights

1. **Larger = Better** (mostly): d12 dominates across all targets
2. **Expected values grow**: d4=3.33, d6=4.20, d8=5.14, d10=6.11, d12=7.09
3. **The d4 paradox**: Explodes most (25%) but has lowest success rates
4. **Non-linear scaling**: Each die size up provides different marginal benefit

### Two Dice Insights

1. **Dramatic improvement**: d6+d6 nearly doubles single d6 odds
2. **d6+d12 optimal**: Best pairing across ALL tested targets
3. **Non-monotonic upgrades**: Sometimes upgrading hurts! (e.g., d4→d6 for target ≥6)
4. **Target-dependent value**: The best upgrade depends on what target you need
5. **The d4 surprise**: Can outperform d6 as second die in certain ranges

### Surprising Results ⚠️

**Cases where upgrading makes things worse:**
- Target ≥6: d6+d4 (32.29%) > d6+d6 (30.56%)
- Target ≥8: d6+d6 (25.85%) > d6+d8 (24.65%)
- Target ≥10: d6+d8 (18.36%) > d6+d10 (17.50%)

These counterintuitive results arise from complex probability interactions!

## 🔧 Running the Code

### Prerequisites
```bash
pip3 install numpy matplotlib
```

### Execution
```bash
python3 exploding_dice.py
```

This will:
1. Calculate all probabilities (single die + two dice)
2. Generate 4 visualization images
3. Print comprehensive results tables
4. Show marginal improvements from upgrades

## 📐 Mathematical Foundation

### Single Die Probability

Recursive formula for P(exploding die ≥ k):
```
P(dN ≥ k) = (direct successes)/N + (1/N) × P(dN ≥ k-N)
```

### Expected Value

For an exploding dN:
```
E[dN] = N(N+1) / (2(N-1))
```

### Maximum of Two Dice

For independent dice X and Y:
```
P(max(X,Y) ≥ k) = 1 - [1 - P(X≥k)] × [1 - P(Y≥k)]
```

## 🎮 Applications

### Tabletop RPG Design
- **Heroic actions**: Use d6+d12 (87% success at ≥4)
- **Medium difficulty**: d6+d8 (25-48% for targets 6-8)
- **Epic challenges**: Even d6+d4 gives 12.6% at ≥10

### Game Balancing
- Understand exact probabilities for player actions
- Design risk/reward systems with predictable outcomes
- Create meaningful choices between die types

### Probability Education
- Demonstrates counterintuitive probability results
- Shows why "more explosions ≠ better outcomes"
- Illustrates independence and maximum operators

## 📈 Visualization Guide

### Bar Charts
- Compare probabilities across die types for each target
- Height = probability of success
- Colors distinguish different dice

### Line Plots
- Show how probability decays with increasing target
- Slope indicates how "steep" the difficulty curve is
- Crossovers reveal interesting transitions

### Heatmaps
- Green = high probability (easy)
- Red = low probability (hard)
- Quickly identify best dice for any target

### Marginal Improvement Plot
- Positive bars = upgrade helps
- Negative bars = upgrade hurts (!)
- Height shows magnitude of change

## 🔬 Technical Details

- **Method**: Exact analytical calculation (not simulation)
- **Accuracy**: Computational precision (no sampling error)
- **Performance**: Sub-second computation for all results
- **Implementation**: Dynamic programming with memoization
- **Language**: Python 3.9+

## 📝 Citation

If you use this analysis in academic or professional work:

```
Exploding Dice Probability Analysis
Method: Analytical calculation using recursive probability formulas
Date: December 19, 2025
Implementation: Python with numpy and matplotlib
```

## 🎓 Further Reading

For those interested in the mathematics:
- **Probability theory**: Independence, conditional probability
- **Recursive formulas**: Dynamic programming solutions
- **Order statistics**: Maximum and minimum of random variables
- **Game theory**: Risk analysis and optimal decision making

## 🚀 Future Extensions

Possible enhancements:
1. **Three or more dice**: Extend to max(d6, d8, d10)
2. **Sum instead of max**: Analyze d6 + d8 (sum, not maximum)
3. **Minimum operator**: Worst of two dice (pessimistic case)
4. **Target ranges**: P(roll between 6 and 10)
5. **Different explosion rules**: Explode on highest K values
6. **Web interface**: Interactive calculator

## ⚖️ License

This analysis is provided for educational and entertainment purposes.

---

## 🎉 Summary

This project demonstrates that:

1. ✅ **Exploding dice can be analyzed exactly** (no simulation needed)
2. ✅ **Larger dice generally perform better** (despite less frequent explosions)
3. ✅ **Two dice dramatically improve odds** (nearly double in many cases)
4. ✅ **Counterintuitive results exist** (upgrades can hurt!)
5. ✅ **Beautiful visualizations** clarify complex probability landscapes

**Explore the analysis documents for deep dives into the mathematics and strategic implications!**

---

*Created: December 19, 2025*  
*Tools: Python, NumPy, Matplotlib*  
*Analysis Type: Exact analytical probability calculations*

