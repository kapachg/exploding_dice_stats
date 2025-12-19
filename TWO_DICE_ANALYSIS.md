# Two Exploding Dice - Maximum Analysis

## Overview

This analysis extends the exploding dice mechanic to **two independent dice**, where we take the **maximum** of their results. One die is always a d6, while the second die varies (d4, d6, d8, d10, d12).

## Mathematical Model

### Maximum of Two Independent Random Variables

For two independent exploding dice X and Y:

**P(max(X, Y) ≥ k) = 1 - P(max(X, Y) < k)**

Since max(X, Y) < k only when both X < k AND Y < k:

**P(max(X, Y) ≥ k) = 1 - P(X < k) · P(Y < k)**

Using the complement rule:

**P(max(X, Y) ≥ k) = 1 - [1 - P(X ≥ k)] · [1 - P(Y ≥ k)]**

This formula allows us to compute the maximum probabilities using the single-die probabilities we already calculated.

### Why the Maximum Improves Probabilities

The maximum operator provides a "best of two attempts" mechanic:
- You succeed if EITHER die reaches the target
- This dramatically increases success rates
- The improvement is largest when probabilities are moderate (not too high or low)

## Complete Results

### Probability Table: P(max(d6, dX) ≥ Target)

| Dice Pair | P(≥4)   | P(≥6)   | P(≥8)   | P(≥10)  |
|-----------|---------|---------|---------|---------|
| **d6+d4** | 62.50%  | 32.29%  | 19.27%  | 12.63%  |
| **d6+d6** | 75.00%  | 30.56%  | 25.85%  | 15.97%  |
| **d6+d8** | 81.25%  | 47.92%  | 24.65%  | 18.36%  |
| **d6+d10**| 85.00%  | 58.33%  | 39.72%  | 17.50%  |
| **d6+d12**| 87.50%  | 65.28%  | 49.77%  | 31.25%  |

### Comparison: Single d6 vs Two Dice

Let's see the dramatic improvement from using two dice:

| Target | Single d6 | d6+d6    | Improvement |
|--------|-----------|----------|-------------|
| ≥4     | 50.00%    | 75.00%   | **+50%**    |
| ≥6     | 16.67%    | 30.56%   | **+83%**    |
| ≥8     | 13.89%    | 25.85%   | **+86%**    |
| ≥10    | 8.33%     | 15.97%   | **+92%**    |

The improvement is **massive** - nearly doubling or more the success rate!

### Marginal Improvements from Upgrading Second Die

How much better does each die upgrade make your chances?

#### Target ≥4:
- d4→d6: **+12.50** percentage points (big jump!)
- d6→d8: **+6.25** pp (good)
- d8→d10: **+3.75** pp (diminishing)
- d10→d12: **+2.50** pp (small)

#### Target ≥6:
- d4→d6: **-1.74** pp (slightly worse! 🤔)
- d6→d8: **+17.36** pp (huge jump!)
- d8→d10: **+10.42** pp (significant)
- d10→d12: **+6.94** pp (worthwhile)

#### Target ≥8:
- d4→d6: **+6.58** pp (good)
- d6→d8: **-1.20** pp (slightly worse!)
- d8→d10: **+15.07** pp (major improvement)
- d10→d12: **+10.05** pp (very good)

#### Target ≥10:
- d4→d6: **+3.34** pp (modest)
- d6→d8: **+2.39** pp (small)
- d8→d10: **-0.86** pp (slightly worse!)
- d10→d12: **+13.75** pp (biggest jump!)

## Surprising Insights

### 1. Non-Monotonic Improvements

**Counterintuitive**: Upgrading your second die doesn't always help!

Examples:
- For target ≥6: d6+d4 (32.29%) actually beats d6+d6 (30.56%)!
- For target ≥8: d6+d6 (25.85%) beats d6+d8 (24.65%)!
- For target ≥10: d6+d8 (18.36%) beats d6+d10 (17.50%)!

**Why?** The interaction between the two dice creates complex probability landscapes. When both dice have similar ranges, they "overlap" more, reducing the benefit.

### 2. The d6+d12 Dominance

For ALL targets, d6+d12 provides the best results:
- ≥4: 87.50% (nearly guaranteed!)
- ≥6: 65.28% (solid odds)
- ≥8: 49.77% (coin flip)
- ≥10: 31.25% (reasonable chance)

This is the optimal pairing among the options tested.

### 3. Target-Dependent Optimal Upgrades

The value of upgrading depends heavily on your target:

**For low targets (≥4)**: 
- Every upgrade helps
- d4→d6 gives best bang for buck

**For medium targets (≥6, ≥8)**:
- d6→d8 provides huge jumps
- But some transitions are negative!

**For high targets (≥10)**:
- d10→d12 provides the largest single improvement (+13.75pp)
- Early upgrades matter less

### 4. When Two d6s Beat Mixed Dice

For certain target ranges, d6+d6 can outperform mixed pairings:
- Better than d6+d8 for target ≥8
- The "symmetry" of identical dice helps in specific ranges

## Visualization Insights

### Panel 1: Bar Chart
- Clear progression: larger second die = higher bars (mostly)
- Target ≥4: All pairings do well (62-88%)
- Target ≥10: Dramatic drop-off, d12 still strong at 31%

### Panel 2: Line Plot
- **d6+d12** (top line): Best overall, gradual decline
- **d6+d4** (bottom line): Weakest, sharp drop
- Lines cross and weave, showing non-monotonic behavior
- Spread increases at higher targets (more variance)

### Panel 3: Marginal Improvement
- **Negative bars**: Upgrades that actually hurt! (fascinating)
- **Tallest positive bars**: Best upgrades to make
- Pattern varies wildly by target
- d10→d12 consistently strong for hard targets

### Heatmap
- **Top row (d6+d12)**: Greenest overall
- **Bottom row (d6+d4)**: More red, especially at high targets
- **Diagonal gradient**: Generally better as you move down-right
- Color transitions show where upgrades matter most

## Mathematical Verification

### Example: P(max(d6, d6) ≥ 6)

Single d6: P(≥6) = 1/6 ≈ 0.1667

```
P(max ≥ 6) = 1 - (1 - 1/6)²
           = 1 - (5/6)²
           = 1 - 25/36
           = 11/36
           ≈ 0.3056 = 30.56% ✓
```

### Example: P(max(d6, d12) ≥ 4)

- P(d6 ≥ 4) = 1/2 = 0.50
- P(d12 ≥ 4) = 3/4 = 0.75

```
P(max ≥ 4) = 1 - (1 - 0.50)(1 - 0.75)
           = 1 - (0.50)(0.25)
           = 1 - 0.125
           = 0.875 = 87.50% ✓
```

### Example: Why d6+d4 > d6+d6 for Target ≥6?

For d6+d4:
- P(d6 ≥ 6) = 1/6 ≈ 0.1667
- P(d4 ≥ 6) = 3/16 = 0.1875 (from explosions)

```
P(max ≥ 6) = 1 - (1 - 1/6)(1 - 3/16)
           = 1 - (5/6)(13/16)
           = 1 - 65/96
           = 31/96
           ≈ 0.3229 = 32.29%
```

For d6+d6:
```
P(max ≥ 6) = 1 - (5/6)²
           = 11/36
           ≈ 0.3056 = 30.56%
```

**d4's explosion frequency** (25% vs d6's 16.67%) gives it an edge in the 6-10 range, even though d6 is "better" on average!

## Strategic Recommendations

### For Game Designers

1. **Guaranteed Success**: Use d6+d12 for "hero moments" (87.5% at ≥4)
2. **Balanced Risk**: d6+d8 or d6+d10 for medium difficulty (25-40% at ≥8)
3. **High Stakes**: Even d6+d4 gives 12.6% at ≥10 (better than nothing!)
4. **Asymmetry**: The non-monotonic improvements create interesting choices

### For Players

1. **Low Targets**: Any pairing works well, even d6+d4
2. **Medium Targets (6-8)**: d8 or larger makes big difference
3. **High Targets (10+)**: You want that d12 (31% vs 12% with d4!)
4. **Risk Profile**: Understand that bigger isn't always better for specific ranges

## Practical Examples

### Example 1: Heroic Action (Target 6)
- d6+d4: 32% (1 in 3 chance)
- d6+d12: 65% (2 in 3 chance)
- **Double your odds** with the right die!

### Example 2: Epic Challenge (Target 10)
- d6 alone: 8% (1 in 12)
- d6+d6: 16% (doubles your chance)
- d6+d12: 31% (quadruples your chance!)

### Example 3: Cost-Benefit
If upgrading from d8→d10 costs resources:
- For target ≥6: Gain +10.4pp (worth it!)
- For target ≥10: Lose -0.9pp (not worth it!)
- **Know your target before upgrading!**

## Comparison to Single Die Results

### Single Die Winners (from Part 1)
| Target | Best Single Die | Probability |
|--------|----------------|-------------|
| ≥4     | d12            | 75.00%      |
| ≥6     | d12            | 58.33%      |
| ≥8     | d12            | 41.67%      |
| ≥10    | d12            | 25.00%      |

### Two Dice Winners (Part 2)
| Target | Best Pairing | Probability | vs Single d12 |
|--------|--------------|-------------|---------------|
| ≥4     | d6+d12       | 87.50%      | +12.5pp       |
| ≥6     | d6+d12       | 65.28%      | +7.0pp        |
| ≥8     | d6+d12       | 49.77%      | +8.1pp        |
| ≥10    | d6+d12       | 31.25%      | +6.3pp        |

**Two dice consistently outperform the best single die by 6-12 percentage points!**

## Technical Implementation

### Maximum Probability Formula
```python
def probability_max_of_two(die1, die2, target):
    p1 = die1.probability_at_least(target)
    p2 = die2.probability_at_least(target)
    return 1 - (1 - p1) * (1 - p2)
```

This elegant formula leverages:
- Independence of dice rolls
- Complement rule for "at least one succeeds"
- Previously computed single-die probabilities

### No Simulation Needed
All results are **exact analytical calculations**, not Monte Carlo simulations. This guarantees:
- Perfect accuracy (no sampling error)
- Fast computation (milliseconds)
- Reproducible results

## Files Generated

1. **exploding_dice.py** - Complete implementation (single + two dice)
2. **two_dice_probabilities.png** - Triple-panel visualization
3. **two_dice_heatmap.png** - Probability heatmap
4. **TWO_DICE_ANALYSIS.md** - This document

## Conclusion

**Key Takeaways:**

1. **Two dice dramatically improve success rates** - Even d6+d6 nearly doubles single d6 odds
2. **d6+d12 is optimal** across all tested targets (87%, 65%, 50%, 31%)
3. **Upgrades aren't always beneficial** - Target-dependent non-monotonic improvements
4. **The d4 surprise** - Sometimes beats d6 as second die due to explosion frequency
5. **Strategic depth** - Understanding these interactions enables sophisticated game design

The maximum-of-two-dice mechanic creates a rich probability landscape with counterintuitive properties, making it ideal for game systems that reward strategic thinking and create memorable moments of triumph and failure.

---

*Analysis completed: December 19, 2025*
*Method: Analytical calculation using independence and complement rules*
*All probabilities exact to computational precision*

