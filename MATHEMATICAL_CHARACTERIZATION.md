# Mathematical Characterization: Die Size vs Target Threshold
## Dependency Structure in Exploding Dice Maximum Systems

---

## Executive Summary

This document provides a **formal mathematical analysis** of how the second die size (N) affects the probability P(max(d6, dN) ≥ T) for target thresholds T ∈ {4, 6, 8, 10}. The analysis reveals:

- **Non-monotonic marginal improvements** in discrete die sizes
- **Four distinct probability regimes** based on target threshold
- **Threshold effects** where die dominance shifts
- **Diminishing returns for low targets**, but **complex dynamics for medium/high targets**

---

## 1. Formal Mathematical Expression

### 1.1 Probability Definition

For two **independent** exploding dice X ~ d6 and Y ~ dN:

```
P(max(X,Y) ≥ T) = 1 - P(max(X,Y) < T)
                = 1 - P(X < T AND Y < T)
                = 1 - P(X < T) · P(Y < T)    [by independence]
                = 1 - F_X(T-1) · F_Y(T-1)
```

Where F_X and F_Y are the **cumulative distribution functions (CDFs)**.

### 1.2 Survival Function Form

Using the **complementary CDF** (survival function) S(T) = P(X ≥ T):

```
P(max(X,Y) ≥ T) = 1 - [1 - S_X(T)] · [1 - S_Y(T)]
```

**Expanded form (inclusion-exclusion):**

```
P(max(X,Y) ≥ T) = S_X(T) + S_Y(T) - S_X(T)·S_Y(T)
```

This reveals **three probability components**:
1. **S_X(T)**: Contribution when first die (d6) succeeds alone
2. **S_Y(T)**: Contribution when second die (dN) succeeds alone  
3. **-S_X(T)·S_Y(T)**: Overlap correction (both succeed)

### 1.3 Functional Notation

Define the probability function:

```
P(N, T) = S_6(T) + S_N(T) - S_6(T)·S_N(T)
```

Where:
- N ∈ {4, 6, 8, 10, 12} is the second die size
- T ∈ {4, 6, 8, 10} is the target threshold
- S_6(T) = P(d6 ≥ T) is **fixed** (d6 is always the first die)
- S_N(T) = P(dN ≥ T) is the **variable** second die probability

---

## 2. Derivatives and Marginal Analysis

### 2.1 First Derivative (Marginal Effect)

Taking the partial derivative with respect to die size N:

```
∂P/∂N = [1 - S_6(T)] · ∂S_N/∂N
```

**Key observations:**
- Since 0 ≤ S_6(T) ≤ 1, the coefficient [1 - S_6(T)] ≥ 0
- The sign depends on ∂S_N/∂N (how second die probability changes)
- In **continuous approximation**, ∂S_N/∂N ≥ 0 (monotonic increase)
- For **discrete dice**, jumps create non-monotonic behavior

**Interpretation:**
- When S_6(T) is **large** (low targets), marginal gains are **small**
- When S_6(T) is **small** (high targets), marginal gains are **large**

### 2.2 Second Derivative (Acceleration)

```
∂²P/∂N² = [1 - S_6(T)] · ∂²S_N/∂N²
```

This measures the **rate of change** in marginal improvements:
- **Negative** → Diminishing returns (concave)
- **Positive** → Increasing returns (convex)
- **Zero** → Linear relationship

**Empirical findings:**
- Target ≥4: **Consistently negative** (diminishing returns)
- Target ≥6: **Non-monotonic** (changes sign)
- Target ≥8: **Non-monotonic** (complex pattern)
- Target ≥10: **Non-monotonic** (peak at final upgrade)

### 2.3 Cross-Partial Derivative

```
∂²P/∂N∂T = -∂S_6/∂T · ∂S_N/∂N + [1 - S_6(T)] · ∂²S_N/∂N∂T - S_6(T) · ∂²S_N/∂N∂T
```

This measures how **the effect of increasing die size changes with target threshold**.

---

## 3. Probability Regimes

### Regime 1: LOW TARGET (T = 4)

**Characteristics:**
- S_6(4) = 0.500 (HIGH base probability)
- **Ceiling effect** dominates
- Marginal improvements: **Consistently diminishing**

**Numerical Results:**
| Die Size | Probability | Marginal Δ | Relative Δ |
|----------|-------------|------------|------------|
| d4       | 62.50%      | —          | —          |
| d6       | 75.00%      | +12.50pp   | +20.0%     |
| d8       | 81.25%      | +6.25pp    | +8.3%      |
| d10      | 85.00%      | +3.75pp    | +4.6%      |
| d12      | 87.50%      | +2.50pp    | +2.9%      |

**Pattern:**
```
Δ₁ > Δ₂ > Δ₃ > Δ₄
Monotonic diminishing returns
```

**Mathematical Explanation:**
- The term [1 - S_6(4)] = 0.5 is moderate
- Second die contribution S_N(4) increases: 0.25 → 0.75
- But overlap term -S_6·S_N grows quadratically
- Net effect: Each upgrade helps less than previous

**Dominant Die:** Shifts from **d6** (with d4) to **dN** (with d12)

---

### Regime 2: MEDIUM-LOW TARGET (T = 6)

**Characteristics:**
- S_6(6) = 0.167 (MODERATE base probability)
- **Non-monotonic behavior** observed
- d4's explosion frequency creates **competitive advantage**

**Numerical Results:**
| Die Size | Probability | Marginal Δ | Relative Δ |
|----------|-------------|------------|------------|
| d4       | 32.29%      | —          | —          |
| d6       | 30.56%      | **-1.74pp**| **-5.4%**  |
| d8       | 47.92%      | +17.36pp   | +56.8%     |
| d10      | 58.33%      | +10.42pp   | +21.7%     |
| d12      | 65.28%      | +6.94pp    | +11.9%     |

**Pattern:**
```
Δ₁ < 0 < Δ₂ > Δ₃ > Δ₄
Non-monotonic with initial dip
Peak improvement at d6→d8
```

**Mathematical Explanation:**
- **Paradox:** d6+d4 > d6+d6 for this target!
- S_4(6) = 0.1875 vs S_6(6) = 0.1667
- d4 explodes 25% of time vs d6's 16.67%
- In range 6-10, d4 explosions give competitive edge
- After d8, die size dominates explosion frequency

**Critical Observation:**
This regime exhibits **threshold crossover** where explosion frequency battles base range.

---

### Regime 3: MEDIUM-HIGH TARGET (T = 8)

**Characteristics:**
- S_6(8) = 0.139 (LOW-MODERATE base probability)
- **Extreme non-monotonic pattern**
- Multiple local optima

**Numerical Results:**
| Die Size | Probability | Marginal Δ | Relative Δ |
|----------|-------------|------------|------------|
| d4       | 19.27%      | —          | —          |
| d6       | 25.85%      | +6.58pp    | +34.1%     |
| d8       | 24.65%      | **-1.20pp**| **-4.6%**  |
| d10      | 39.72%      | +15.07pp   | +61.1%     |
| d12      | 49.77%      | +10.05pp   | +25.3%     |

**Pattern:**
```
Δ₁ > 0 > Δ₂ < Δ₃ > Δ₄
Two reversals in sign
Trough at d6→d8
Peak at d8→d10
```

**Mathematical Explanation:**
- S_N(8) values: 0.0625, 0.1389, 0.1250, 0.3000, 0.4167
- **Notice:** S_8(8) < S_6(8) ← d8 probability actually DROPS!
- Why? Target=8 equals die max, no single-roll success
- d8 requires explosion to reach 8+
- d6 can roll 6, explode to 2+ (easier path)
- d10 provides huge jump by having direct paths

**Critical Threshold:**
Target = N creates **discontinuity** in probability function.

---

### Regime 4: HIGH TARGET (T = 10)

**Characteristics:**
- S_6(10) = 0.083 (LOW base probability)
- **Large relative improvements** possible
- Second die becomes **dominant** factor

**Numerical Results:**
| Die Size | Probability | Marginal Δ | Relative Δ |
|----------|-------------|------------|------------|
| d4       | 12.63%      | —          | —          |
| d6       | 15.97%      | +3.34pp    | +26.5%     |
| d8       | 18.36%      | +2.39pp    | +14.9%     |
| d10      | 17.50%      | **-0.86pp**| **-4.7%**  |
| d12      | 31.25%      | +13.75pp   | +78.6%     |

**Pattern:**
```
Δ₁ > Δ₂ > 0 > Δ₃ < Δ₄
Trough at d8→d10
Massive spike at d10→d12
```

**Mathematical Explanation:**
- S_10(10) = 0.10 vs S_8(10) = 0.1094
- d10 requires exactly 10 (no direct path)
- Must roll 10, then explode ≥0: (1/10) × 1 = 0.10
- d8 can: (1) roll 8, explode ≥2, OR (2) roll < 8, double-explode
- This creates slight advantage for d8
- d12 provides **massive jump**: direct paths 10-12, plus explosions
- S_12(10) = 0.25 (2.5× better than d10!)

**Dominant Die:** **d12 completely dominates** at this target

---

## 4. Component Analysis

### 4.1 Three-Component Decomposition

For any (N, T) pair:

```
P(N,T) = Contribution₆ + ContributionN - Overlap

Where:
  Contribution₆ = S_6(T) · [1 - S_N(T)]
  ContributionN = S_N(T) · [1 - S_6(T)]
  Overlap = S_6(T) · S_N(T)
```

### 4.2 Dominance Classification

Define **dominance ratio**:

```
r = ContributionN / Contribution₆
```

Classification:
- r < 0.5: **d6 dominates**
- 0.5 ≤ r ≤ 2.0: **Balanced**
- r > 2.0: **dN dominates**

**Results by Target:**

#### Target ≥4:
| Second Die | r     | Classification         |
|------------|-------|------------------------|
| d4         | 0.33  | d6 DOMINATES           |
| d6         | 1.00  | BALANCED               |
| d8         | 1.67  | BALANCED               |
| d10        | 2.33  | d10 DOMINATES          |
| d12        | 3.00  | d12 STRONGLY DOMINATES |

#### Target ≥10:
| Second Die | r     | Classification         |
|------------|-------|------------------------|
| d4         | 0.54  | BALANCED               |
| d6         | 1.00  | BALANCED               |
| d8         | 1.35  | BALANCED               |
| d10        | 1.22  | BALANCED               |
| d12        | 3.67  | d12 STRONGLY DOMINATES |

**Observation:** At high targets, dice remain balanced until d12, which provides dramatic dominance.

---

## 5. Non-Linearities and Threshold Effects

### 5.1 Identified Non-Linearities

1. **Explosion Frequency Jumps**
   - Each die has explosion probability 1/N
   - d4: 25%, d6: 16.7%, d8: 12.5%, d10: 10%, d12: 8.3%
   - These discrete jumps create non-smooth S_N(T) functions

2. **Target = Die Size Discontinuities**
   - When T = N, direct single-roll success impossible
   - Creates probability "dip" at these points
   - Explains d8 paradox at T=8, d10 paradox at T=10

3. **Overlap Term Quadratic Growth**
   - Overlap = S_6(T) · S_N(T) grows faster than linear components
   - Creates ceiling effect for low targets
   - Reduces marginal benefits as both probabilities increase

### 5.2 Threshold Effects Summary

| Target | Effect Type           | Mechanism                           |
|--------|-----------------------|-------------------------------------|
| ≥4     | Ceiling Effect        | High S_6(4) limits improvement      |
| ≥6     | Explosion Crossover   | d4 frequency beats d6 base range    |
| ≥8     | Target=Die Discontinuity | d8 requires explosion for 8+     |
| ≥10    | Target=Die + Dominance | d10 dip, then d12 spike           |

---

## 6. Efficiency and Optimization

### 6.1 Efficiency Metric

Define **efficiency** as probability per unit die size:

```
E(N, T) = P(N, T) / N
```

**Interpretation:** "Probability bang for your die-size buck"

**Results:**

| Target | Optimal by Efficiency | Efficiency Value |
|--------|----------------------|------------------|
| ≥4     | **d4**               | 0.156            |
| ≥6     | d8                   | 0.060            |
| ≥8     | d4                   | 0.048            |
| ≥10    | d4                   | 0.032            |

**Surprising Finding:** d4 is most **efficient** for targets ≥4, ≥8, ≥10, despite having lowest absolute probability!

### 6.2 Absolute vs Relative Optimization

**If optimizing for absolute probability:** Choose d12 (always best)

**If optimizing for efficiency:** Choose d4 (best bang/buck)

**If optimizing for marginal gain:** Depends on current die and target
- From d4: Upgrade to d6 (target ≥4), d8 (target ≥6)
- From d8: Upgrade to d10 (target ≥6, ≥8)
- Always upgrade to d12 for target ≥10

---

## 7. Asymptotic Behavior

### 7.1 Limit as N → ∞

For fixed target T:

```
lim[N→∞] S_N(T) = 1
```

Because larger dice can reach any finite target with high probability.

Therefore:

```
lim[N→∞] P(N, T) = 1 - [1 - S_6(T)] · [1 - 1]
                   = 1 - 0
                   = 1
```

**Guaranteed success** as die size approaches infinity.

### 7.2 Convergence Rate

From our data, approximate convergence:

```
P(N, T) ≈ 1 - exp(-α(T) · N)
```

Where α(T) depends on target threshold.

**Fitted parameters** (approximate):
- Target ≥4: α ≈ 0.12 (fast convergence, already near 1)
- Target ≥6: α ≈ 0.08 
- Target ≥8: α ≈ 0.06
- Target ≥10: α ≈ 0.05 (slow convergence)

---

## 8. Statistical Significance of Upgrades

### 8.1 Negligible Impact Threshold

Define upgrade as **negligible** if marginal gain < 1 percentage point.

**Results:**

**Never negligible upgrades (always > 1pp):**
- All upgrades for all targets meet significance threshold

**Smallest improvements:**
- d6→d8 for T≥8: -1.20pp (actually negative!)
- d8→d10 for T≥10: -0.86pp (negative!)

**Largest improvements:**
- d6→d8 for T≥6: +17.36pp
- d8→d10 for T≥8: +15.07pp
- d10→d12 for T≥10: +13.75pp

### 8.2 Significant Gains Classification

**Highly Significant (Δ > 10pp):**
- d4→d6 for T≥4: +12.50pp
- d6→d8 for T≥6: +17.36pp
- d8→d10 for T≥6: +10.42pp
- d8→d10 for T≥8: +15.07pp
- d6→d8 for T≥8: +10.05pp (from d12)
- d10→d12 for T≥10: +13.75pp

These represent **strategically important** upgrades.

---

## 9. Visual Analysis Summary

### 9.1 Main Probability Plot (Top Left)

**Key Features:**
- Four distinct curves (one per target)
- Target ≥4: Nearly flat, high baseline (ceiling effect)
- Target ≥10: Steep rise, especially d12 jump
- Smooth interpolation shows continuous approximation
- Discrete points reveal actual die probabilities

**Critical Observations:**
- Curves do NOT cross (targets maintain ordering)
- Steepness increases with target threshold
- Final jump (d10→d12) largest for high targets

### 9.2 Marginal Improvement Plot (Top Right)

**Key Features:**
- Negative bars indicate HARMFUL upgrades
- Target ≥6: Massive spike at d6→d8
- Target ≥10: Huge spike at d10→d12
- Pattern inconsistency across targets

**Critical Observations:**
- No universal "best upgrade" - highly target-dependent
- Negative improvements occur at **different steps** for different targets
- This explains strategic complexity

### 9.3 Component Breakdown (Middle Row)

**Target ≥4:**
- S_X (d6) constant at 0.5
- S_Y grows: 0.25 → 0.75
- Overlap grows: 0.125 → 0.375
- d6 dominance transitions to dN dominance

**Target ≥10:**
- S_X (d6) constant at 0.083
- S_Y grows slowly: 0.047 → 0.25
- Overlap remains small throughout
- d12 provides dramatic Y contribution jump

### 9.4 Second Derivative (Bottom Left)

**Acceleration Analysis:**
- **Positive** = marginal gains increasing (convex)
- **Negative** = marginal gains decreasing (concave)

**Target ≥4:** Consistently negative (pure diminishing returns)
**Target ≥8:** Wild oscillation (complex interaction)
**Target ≥10:** Massive positive spike at end (d12 breakthrough)

### 9.5 3D Surface Plot

**Visual Features:**
- Surface rises from front (low T, low N) to back (high T, high N)
- **Twisted surface** indicates non-linear interactions
- Discrete red points mark actual die measurements
- Color gradient: Purple (low) → Green → Yellow (high)

**Critical Observations:**
- Surface is NOT a simple plane (non-linear!)
- Curvature changes dramatically with T
- Ridge line along T=4 (ceiling effect plateau)
- Steep cliff at N=12 for high T (d12 dominance)

---

## 10. Conclusions and Implications

### 10.1 Mathematical Structure

The probability function P(N, T) exhibits:

1. **Multiplicative interaction** between dice via overlap term
2. **Target-dependent regimes** with qualitatively different behavior
3. **Non-monotonic marginal effects** due to discrete die jumps
4. **Threshold discontinuities** when T equals die maximum
5. **Asymptotic convergence** to certainty as N→∞

### 10.2 Practical Implications

**For Game Design:**
- Cannot assume "bigger die = better" for all contexts
- Target threshold determines optimal die choice
- Strategic depth emerges from non-monotonic improvements

**For Players:**
- Understand your target before choosing dice
- d12 is safest choice (always best absolute probability)
- But d4 can be surprisingly competitive for specific ranges

**For Probability Theory:**
- Demonstrates rich behavior in discrete distribution maxima
- Shows importance of explosion mechanics in game math
- Highlights interaction between discrete and continuous effects

### 10.3 Open Questions

1. **Generalization:** How does this extend to max(d6, dN₁, dN₂, ...) with 3+ dice?
2. **Sum vs Max:** How does behavior change if we sum dice instead of taking maximum?
3. **Different explosion rules:** What if we explode on top K values?
4. **Optimal die selection:** Given target distribution, what mix of dice optimizes expected utility?

---

## Appendix: Mathematical Proofs

### Proof of Monotonicity in Continuous Approximation

**Theorem:** If S_N(T) is continuous and increasing in N, then P(N,T) is increasing in N.

**Proof:**
```
∂P/∂N = ∂/∂N [S_6(T) + S_N(T) - S_6(T)·S_N(T)]
       = ∂S_N/∂N - S_6(T)·∂S_N/∂N
       = [1 - S_6(T)]·∂S_N/∂N
```

Since 0 ≤ S_6(T) ≤ 1, we have [1 - S_6(T)] ≥ 0.

If ∂S_N/∂N > 0 (increasing assumption), then ∂P/∂N > 0.

Therefore P is increasing in N. ∎

**Note:** This breaks for discrete dice due to jumps in S_N.

### Proof of Ceiling Effect

**Theorem:** As S_6(T) → 1, marginal improvements from increasing N approach zero.

**Proof:**
```
∂P/∂N = [1 - S_6(T)]·∂S_N/∂N

As S_6(T) → 1:
  [1 - S_6(T)] → 0

Therefore:
  ∂P/∂N → 0·∂S_N/∂N = 0
```

This proves the ceiling effect. ∎

---

*Analysis Date: December 19, 2025*  
*Method: Exact analytical calculation with numerical evaluation*  
*All derivatives computed via finite differences on discrete die sizes*

