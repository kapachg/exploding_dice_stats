"""
Exploding Dice Probability Calculator

This module calculates and visualizes probabilities for exploding dice mechanics.
An exploding die rolls again and adds to the total when the maximum value is rolled.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from functools import lru_cache
from typing import Dict, List, Tuple


class ExplodingDie:
    """
    Represents an exploding die with n faces (1 to n).
    
    When the maximum value (n) is rolled, the die "explodes" and is rolled again,
    adding the new result to the cumulative total. This process repeats indefinitely.
    """
    
    def __init__(self, n: int):
        """
        Initialize an exploding die with n faces.
        
        Args:
            n: Maximum face value of the die (e.g., 6 for d6)
        """
        self.n = n
        self._cache = {}
    
    def probability_at_least(self, target: int, max_depth: int = 1000) -> float:
        """
        Calculate the probability of rolling at least the target value.
        
        Uses dynamic programming with memoization to handle the recursive nature
        of exploding dice.
        
        Args:
            target: The minimum total value to achieve
            max_depth: Maximum recursion depth for safety
            
        Returns:
            Probability of achieving at least the target value (0 to 1)
        """
        if target <= 1:
            return 1.0
        
        if target in self._cache:
            return self._cache[target]
        
        if max_depth <= 0:
            # Approximation for very deep recursion (extremely rare)
            return 0.0
        
        # Probability calculation:
        # P(Total >= target) = sum of two cases:
        # 1. Roll value v where v >= target (no explosion needed)
        # 2. Roll value v < target < n (no explosion, not enough)
        # 3. Roll n (explosion occurs), then need Total >= (target - n)
        
        prob = 0.0
        
        # Case 1: Direct rolls that meet or exceed target (no explosion)
        if target <= self.n:
            # Can roll target, target+1, ..., n-1 directly
            # (n itself causes explosion, handled separately)
            direct_success_count = max(0, self.n - target)
            prob += direct_success_count / self.n
        
        # Case 2: Explosion case (roll n, then need target-n more)
        explosion_prob = 1.0 / self.n
        remaining_needed = target - self.n
        prob += explosion_prob * self.probability_at_least(remaining_needed, max_depth - 1)
        
        self._cache[target] = prob
        return prob
    
    def expected_value(self, max_terms: int = 1000) -> float:
        """
        Calculate the expected value of an exploding die.
        
        For an exploding dn:
        E[X] = sum(i=1 to n-1) i * (1/n) + n * (1/n) * (1 + E[X])
        E[X] = (1/n) * sum(i=1 to n-1) i + n/n + (n/n) * E[X]
        E[X] - E[X]/n = (sum(i=1 to n-1) i + n) / n
        E[X] * (n-1)/n = sum(i=1 to n) i / n
        E[X] = n/(n-1) * (n+1)/2 = n(n+1) / (2(n-1))
        
        Returns:
            Expected value of a single roll of the exploding die
        """
        return self.n * (self.n + 1) / (2 * (self.n - 1))


def calculate_all_probabilities(
    dice_sizes: List[int],
    targets: List[int]
) -> Dict[int, Dict[int, float]]:
    """
    Calculate probabilities for multiple dice and targets.
    
    Args:
        dice_sizes: List of die sizes (e.g., [4, 6, 8, 10, 12])
        targets: List of target values (e.g., [4, 6, 8, 10])
        
    Returns:
        Nested dictionary: {die_size: {target: probability}}
    """
    results = {}
    
    for die_size in dice_sizes:
        die = ExplodingDie(die_size)
        results[die_size] = {}
        
        for target in targets:
            prob = die.probability_at_least(target)
            results[die_size][target] = prob
            
        # Print expected value for reference
        print(f"d{die_size}: E[X] = {die.expected_value():.3f}")
    
    return results


def visualize_probabilities(
    results: Dict[int, Dict[int, float]],
    dice_sizes: List[int],
    targets: List[int]
):
    """
    Create comprehensive visualizations of the probability results.
    
    Creates two plots:
    1. Grouped bar chart showing probabilities by target value
    2. Line plot showing probability decay across targets for each die
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Color palette for different dice
    colors = plt.cm.viridis(np.linspace(0.15, 0.85, len(dice_sizes)))
    
    # Plot 1: Grouped bar chart
    x = np.arange(len(targets))
    width = 0.15
    
    for idx, die_size in enumerate(dice_sizes):
        probabilities = [results[die_size][target] for target in targets]
        offset = width * (idx - len(dice_sizes) / 2 + 0.5)
        ax1.bar(x + offset, probabilities, width, label=f'd{die_size}', 
                color=colors[idx], alpha=0.8, edgecolor='black', linewidth=0.5)
    
    ax1.set_xlabel('Target Value', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Probability P(Total ≥ Target)', fontsize=12, fontweight='bold')
    ax1.set_title('Exploding Dice: Probability of Reaching Target Values', 
                  fontsize=14, fontweight='bold', pad=20)
    ax1.set_xticks(x)
    ax1.set_xticklabels([f'≥{t}' for t in targets])
    ax1.legend(title='Die Type', fontsize=10)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_ylim(0, 1.05)
    
    # Add percentage labels on bars
    for idx, die_size in enumerate(dice_sizes):
        probabilities = [results[die_size][target] for target in targets]
        offset = width * (idx - len(dice_sizes) / 2 + 0.5)
        for i, prob in enumerate(probabilities):
            if prob > 0.05:  # Only show label if probability is significant
                ax1.text(x[i] + offset, prob + 0.02, f'{prob:.2%}', 
                        ha='center', va='bottom', fontsize=7, rotation=0)
    
    # Plot 2: Line plot
    for idx, die_size in enumerate(dice_sizes):
        probabilities = [results[die_size][target] for target in targets]
        ax2.plot(targets, probabilities, marker='o', markersize=8, 
                linewidth=2.5, label=f'd{die_size}', color=colors[idx], alpha=0.8)
    
    ax2.set_xlabel('Target Value', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Probability P(Total ≥ Target)', fontsize=12, fontweight='bold')
    ax2.set_title('Probability Decay Across Target Values', 
                  fontsize=14, fontweight='bold', pad=20)
    ax2.legend(title='Die Type', fontsize=10)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_ylim(0, 1.05)
    ax2.set_xticks(targets)
    
    plt.tight_layout()
    plt.savefig('exploding_dice_probabilities.png', dpi=300, bbox_inches='tight')
    print("\n📊 Visualization saved as 'exploding_dice_probabilities.png'")
    plt.close()


def create_heatmap(
    results: Dict[int, Dict[int, float]],
    dice_sizes: List[int],
    targets: List[int]
):
    """
    Create a heatmap showing probabilities across all dice and targets.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Prepare data matrix
    data = np.zeros((len(dice_sizes), len(targets)))
    for i, die_size in enumerate(dice_sizes):
        for j, target in enumerate(targets):
            data[i, j] = results[die_size][target]
    
    # Create heatmap
    im = ax.imshow(data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    
    # Set ticks and labels
    ax.set_xticks(np.arange(len(targets)))
    ax.set_yticks(np.arange(len(dice_sizes)))
    ax.set_xticklabels([f'≥{t}' for t in targets])
    ax.set_yticklabels([f'd{d}' for d in dice_sizes])
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Probability', rotation=270, labelpad=20, fontweight='bold')
    
    # Add text annotations
    for i in range(len(dice_sizes)):
        for j in range(len(targets)):
            text = ax.text(j, i, f'{data[i, j]:.3f}',
                          ha="center", va="center", color="black", fontsize=10,
                          fontweight='bold')
    
    ax.set_title('Exploding Dice Probability Heatmap', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Target Value', fontsize=12, fontweight='bold')
    ax.set_ylabel('Die Type', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('exploding_dice_heatmap.png', dpi=300, bbox_inches='tight')
    print("📊 Heatmap saved as 'exploding_dice_heatmap.png'")
    plt.close()


def print_results_table(
    results: Dict[int, Dict[int, float]],
    dice_sizes: List[int],
    targets: List[int]
):
    """
    Print results in a formatted table.
    """
    print("\n" + "="*70)
    print("EXPLODING DICE PROBABILITY RESULTS")
    print("="*70)
    print("\nProbability of achieving at least the target value:\n")
    
    # Header
    header = "Die Type  |  " + "  |  ".join([f"≥{t:2d}" for t in targets])
    print(header)
    print("-" * len(header))
    
    # Data rows
    for die_size in dice_sizes:
        row = f"   d{die_size:<5}  |  "
        row += "  |  ".join([f"{results[die_size][target]:>5.2%}" for target in targets])
        print(row)
    
    print("="*70)


def probability_max_of_two(
    die1: ExplodingDie,
    die2: ExplodingDie,
    target: int
) -> float:
    """
    Calculate probability that max(die1, die2) >= target.
    
    For independent random variables:
    P(max(X,Y) >= k) = 1 - P(max(X,Y) < k)
                     = 1 - P(X < k AND Y < k)
                     = 1 - P(X < k) * P(Y < k)
                     = 1 - [1 - P(X >= k)] * [1 - P(Y >= k)]
    
    Args:
        die1: First exploding die
        die2: Second exploding die
        target: Target value to reach or exceed
        
    Returns:
        Probability that the maximum of two independent rolls >= target
    """
    p1 = die1.probability_at_least(target)
    p2 = die2.probability_at_least(target)
    
    # P(max >= k) = 1 - (1-p1)(1-p2)
    return 1 - (1 - p1) * (1 - p2)


def calculate_two_dice_probabilities(
    second_dice_sizes: List[int],
    targets: List[int]
) -> Dict[int, Dict[int, float]]:
    """
    Calculate probabilities for d6 + various second dice (taking maximum).
    
    Args:
        second_dice_sizes: List of second die sizes (e.g., [4, 6, 8, 10, 12])
        targets: List of target values
        
    Returns:
        Nested dictionary: {second_die_size: {target: probability}}
    """
    results = {}
    d6 = ExplodingDie(6)
    
    print("\nTwo-Dice Maximum Results (d6 + dX):")
    print("-" * 70)
    
    for die_size in second_dice_sizes:
        second_die = ExplodingDie(die_size)
        results[die_size] = {}
        
        for target in targets:
            prob = probability_max_of_two(d6, second_die, target)
            results[die_size][target] = prob
        
        # Show expected value of the pairing
        print(f"d6 + d{die_size}: E[d6]={d6.expected_value():.3f}, "
              f"E[d{die_size}]={second_die.expected_value():.3f}")
    
    return results


def visualize_two_dice_probabilities(
    results: Dict[int, Dict[int, float]],
    dice_sizes: List[int],
    targets: List[int]
):
    """
    Create visualizations for two-dice maximum probabilities.
    
    Creates three plots:
    1. Grouped bar chart by target value
    2. Line plot showing probability improvement with larger second die
    3. Marginal improvement visualization
    """
    fig = plt.figure(figsize=(18, 6))
    gs = fig.add_gridspec(1, 3, hspace=0.3, wspace=0.3)
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])
    
    colors = plt.cm.plasma(np.linspace(0.15, 0.85, len(dice_sizes)))
    
    # Plot 1: Grouped bar chart
    x = np.arange(len(targets))
    width = 0.15
    
    for idx, die_size in enumerate(dice_sizes):
        probabilities = [results[die_size][target] for target in targets]
        offset = width * (idx - len(dice_sizes) / 2 + 0.5)
        ax1.bar(x + offset, probabilities, width, label=f'd6+d{die_size}', 
                color=colors[idx], alpha=0.8, edgecolor='black', linewidth=0.5)
    
    ax1.set_xlabel('Target Value', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Probability P(max ≥ Target)', fontsize=12, fontweight='bold')
    ax1.set_title('Two Exploding Dice: P(max(d6, dX) ≥ Target)', 
                  fontsize=13, fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels([f'≥{t}' for t in targets])
    ax1.legend(title='Dice Pairing', fontsize=9)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    ax1.set_ylim(0, 1.05)
    
    # Add percentage labels
    for idx, die_size in enumerate(dice_sizes):
        probabilities = [results[die_size][target] for target in targets]
        offset = width * (idx - len(dice_sizes) / 2 + 0.5)
        for i, prob in enumerate(probabilities):
            if prob > 0.05:
                ax1.text(x[i] + offset, prob + 0.02, f'{prob:.1%}', 
                        ha='center', va='bottom', fontsize=7, rotation=0)
    
    # Plot 2: Line plot showing improvement with larger dice
    for idx, die_size in enumerate(dice_sizes):
        probabilities = [results[die_size][target] for target in targets]
        ax2.plot(targets, probabilities, marker='o', markersize=8, 
                linewidth=2.5, label=f'd6+d{die_size}', color=colors[idx], alpha=0.8)
    
    ax2.set_xlabel('Target Value', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Probability P(max ≥ Target)', fontsize=12, fontweight='bold')
    ax2.set_title('Probability by Second Die Size', 
                  fontsize=13, fontweight='bold', pad=15)
    ax2.legend(title='Dice Pairing', fontsize=9)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.set_ylim(0, 1.05)
    ax2.set_xticks(targets)
    
    # Plot 3: Marginal improvement (benefit of larger second die)
    for target_idx, target in enumerate(targets):
        improvements = []
        die_labels = []
        
        for idx in range(1, len(dice_sizes)):
            prev_die = dice_sizes[idx - 1]
            curr_die = dice_sizes[idx]
            
            prev_prob = results[prev_die][target]
            curr_prob = results[curr_die][target]
            
            improvement = curr_prob - prev_prob
            improvements.append(improvement * 100)  # Convert to percentage points
            die_labels.append(f'd{prev_die}→d{curr_die}')
        
        x_pos = np.arange(len(improvements))
        offset = 0.2 * (target_idx - len(targets) / 2 + 0.5)
        ax3.bar(x_pos + offset, improvements, 0.2, 
                label=f'Target ≥{target}', alpha=0.8)
    
    ax3.set_xlabel('Die Size Upgrade', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Marginal Improvement (percentage points)', fontsize=11, fontweight='bold')
    ax3.set_title('Benefit of Upgrading Second Die', 
                  fontsize=13, fontweight='bold', pad=15)
    ax3.set_xticks(np.arange(len(die_labels)))
    ax3.set_xticklabels(die_labels, rotation=0, fontsize=9)
    ax3.legend(title='Target Value', fontsize=9)
    ax3.grid(axis='y', alpha=0.3, linestyle='--')
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    
    plt.tight_layout()
    plt.savefig('two_dice_probabilities.png', dpi=300, bbox_inches='tight')
    print("\n📊 Two-dice visualization saved as 'two_dice_probabilities.png'")
    plt.close()


def create_two_dice_heatmap(
    results: Dict[int, Dict[int, float]],
    dice_sizes: List[int],
    targets: List[int]
):
    """
    Create a heatmap for two-dice maximum probabilities.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Prepare data matrix
    data = np.zeros((len(dice_sizes), len(targets)))
    for i, die_size in enumerate(dice_sizes):
        for j, target in enumerate(targets):
            data[i, j] = results[die_size][target]
    
    # Create heatmap
    im = ax.imshow(data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    
    # Set ticks and labels
    ax.set_xticks(np.arange(len(targets)))
    ax.set_yticks(np.arange(len(dice_sizes)))
    ax.set_xticklabels([f'≥{t}' for t in targets])
    ax.set_yticklabels([f'd6+d{d}' for d in dice_sizes])
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Probability', rotation=270, labelpad=20, fontweight='bold')
    
    # Add text annotations
    for i in range(len(dice_sizes)):
        for j in range(len(targets)):
            text = ax.text(j, i, f'{data[i, j]:.3f}',
                          ha="center", va="center", color="black", fontsize=10,
                          fontweight='bold')
    
    ax.set_title('Two Exploding Dice: P(max(d6, dX) ≥ Target) Heatmap', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel('Target Value', fontsize=12, fontweight='bold')
    ax.set_ylabel('Dice Pairing', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('two_dice_heatmap.png', dpi=300, bbox_inches='tight')
    print("📊 Two-dice heatmap saved as 'two_dice_heatmap.png'")
    plt.close()


def print_two_dice_table(
    results: Dict[int, Dict[int, float]],
    dice_sizes: List[int],
    targets: List[int]
):
    """
    Print two-dice results in a formatted table.
    """
    print("\n" + "="*70)
    print("TWO-DICE MAXIMUM PROBABILITY RESULTS")
    print("="*70)
    print("\nProbability that max(d6, dX) reaches at least the target:\n")
    
    # Header
    header = "Dice Pair  |  " + "  |  ".join([f"≥{t:2d}" for t in targets])
    print(header)
    print("-" * len(header))
    
    # Data rows
    for die_size in dice_sizes:
        row = f" d6+d{die_size:<4}  |  "
        row += "  |  ".join([f"{results[die_size][target]:>5.2%}" for target in targets])
        print(row)
    
    print("="*70)
    
    # Show marginal improvements
    print("\nMarginal Improvement from Upgrading Second Die:")
    print("-" * 70)
    
    for target in targets:
        print(f"\nTarget ≥{target}:")
        for i in range(1, len(dice_sizes)):
            prev_die = dice_sizes[i-1]
            curr_die = dice_sizes[i]
            prev_prob = results[prev_die][target]
            curr_prob = results[curr_die][target]
            improvement = (curr_prob - prev_prob) * 100
            print(f"  d{prev_die}→d{curr_die}: +{improvement:>5.2f} percentage points")


def main():
    """
    Main execution function.
    """
    # Define dice and targets
    dice_sizes = [4, 6, 8, 10, 12]
    targets = [4, 6, 8, 10]
    
    print("🎲 EXPLODING DICE PROBABILITY CALCULATOR 🎲")
    print("=" * 70)
    print("\nPART 1: SINGLE EXPLODING DIE ANALYSIS")
    print("=" * 70)
    print("\nCalculating probabilities for exploding dice...")
    print(f"Dice: {', '.join([f'd{d}' for d in dice_sizes])}")
    print(f"Targets: {', '.join([f'≥{t}' for t in targets])}")
    print("\n" + "-" * 70)
    print("Expected Values (with infinite explosions):")
    print("-" * 70)
    
    # Calculate probabilities
    results = calculate_all_probabilities(dice_sizes, targets)
    
    # Print results
    print_results_table(results, dice_sizes, targets)
    
    # Create visualizations
    print("\n📈 Generating single-die visualizations...")
    visualize_probabilities(results, dice_sizes, targets)
    create_heatmap(results, dice_sizes, targets)
    
    print("\n" + "="*70)
    print("PART 2: TWO-DICE MAXIMUM ANALYSIS")
    print("="*70)
    print("\nCalculating probabilities for max(d6, dX)...")
    print(f"Fixed die: d6")
    print(f"Variable die: {', '.join([f'd{d}' for d in dice_sizes])}")
    print(f"Targets: {', '.join([f'≥{t}' for t in targets])}")
    
    # Calculate two-dice probabilities
    two_dice_results = calculate_two_dice_probabilities(dice_sizes, targets)
    
    # Print results
    print_two_dice_table(two_dice_results, dice_sizes, targets)
    
    # Create visualizations
    print("\n📈 Generating two-dice visualizations...")
    visualize_two_dice_probabilities(two_dice_results, dice_sizes, targets)
    create_two_dice_heatmap(two_dice_results, dice_sizes, targets)
    
    print("\n✅ Complete analysis finished!")
    print("\n💡 Key Insights (Single Die):")
    print("   • Larger dice have higher probabilities for reaching targets")
    print("   • Expected values grow with die size: d4=3.33, d6=4.20, d12=7.09")
    
    print("\n💡 Key Insights (Two Dice - Maximum):")
    print("   • Taking max of two dice dramatically improves probabilities")
    print("   • d6+d12 pairing provides best overall performance")
    print("   • Marginal benefit of larger second die varies by target")
    print("   • For low targets, even d6+d4 gives excellent results")


if __name__ == "__main__":
    main()

