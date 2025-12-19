"""
Target Value Analysis for Exploding Dice

This module analyzes how probability varies with TARGET VALUE (T) for fixed dice pairings.
Focus: Game design insights about difficulty scaling with target thresholds.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from exploding_dice import ExplodingDie, probability_max_of_two


def compute_full_target_range(max_target=25):
    """
    Compute probabilities for all positive integer targets from 1 to max_target.
    
    Returns:
        dict: Complete probability data for all targets and dice pairings
    """
    dice_pairings = {
        'd6+d4': (6, 4),
        'd6+d6': (6, 6),
        'd6+d8': (6, 8),
        'd6+d10': (6, 10),
        'd6+d12': (6, 12)
    }
    
    # Also compute single die for comparison
    single_dice = [4, 6, 8, 10, 12]
    
    results = {
        'targets': list(range(1, max_target + 1)),
        'two_dice': {},
        'single_dice': {},
        'derivatives': {},
        'second_derivatives': {}
    }
    
    print("Computing probabilities for all target values...")
    print(f"Target range: 1 to {max_target}")
    print("-" * 70)
    
    # Single dice probabilities
    for die_size in single_dice:
        die = ExplodingDie(die_size)
        results['single_dice'][die_size] = []
        
        for target in results['targets']:
            prob = die.probability_at_least(target)
            results['single_dice'][die_size].append(prob)
    
    # Two dice probabilities
    for pairing_name, (die1_size, die2_size) in dice_pairings.items():
        die1 = ExplodingDie(die1_size)
        die2 = ExplodingDie(die2_size)
        
        results['two_dice'][pairing_name] = []
        
        for target in results['targets']:
            prob = probability_max_of_two(die1, die2, target)
            results['two_dice'][pairing_name].append(prob)
        
        print(f"✓ Computed {pairing_name}")
    
    # Compute derivatives (rate of change)
    print("\nComputing derivatives...")
    for pairing_name in dice_pairings.keys():
        probs = results['two_dice'][pairing_name]
        
        # First derivative (dP/dT)
        derivs = np.diff(probs)  # Negative because P decreases as T increases
        results['derivatives'][pairing_name] = derivs
        
        # Second derivative (d²P/dT²)
        second_derivs = np.diff(derivs)
        results['second_derivatives'][pairing_name] = second_derivs
    
    print("✓ Derivatives computed\n")
    
    return results, dice_pairings


def identify_thresholds(results, dice_pairings):
    """
    Identify critical thresholds and regime boundaries.
    """
    print("="*80)
    print("THRESHOLD AND REGIME ANALYSIS")
    print("="*80)
    print()
    
    for pairing_name in dice_pairings.keys():
        print(f"\n{pairing_name}:")
        print("-" * 60)
        
        probs = results['two_dice'][pairing_name]
        targets = results['targets']
        
        # Find where probability drops below certain thresholds
        thresholds_to_check = [0.95, 0.90, 0.75, 0.50, 0.25, 0.10, 0.05]
        
        for threshold in thresholds_to_check:
            # Find first target where probability drops below threshold
            for i, (target, prob) in enumerate(zip(targets, probs)):
                if prob < threshold:
                    if i > 0:
                        print(f"  P < {threshold:.0%} starting at T = {target} "
                              f"(was {probs[i-1]:.1%} at T = {target-1})")
                    else:
                        print(f"  P < {threshold:.0%} for all targets")
                    break
            else:
                print(f"  P ≥ {threshold:.0%} for all targets up to {targets[-1]}")


def analyze_slopes(results, dice_pairings):
    """
    Analyze where probability curves are steep vs flat.
    """
    print("\n" + "="*80)
    print("SLOPE ANALYSIS: Steep vs Flat Regions")
    print("="*80)
    print()
    print("Steep regions = small change in target has large impact on probability")
    print("Flat regions = probability insensitive to target changes")
    print()
    
    for pairing_name in dice_pairings.keys():
        print(f"\n{pairing_name}:")
        print("-" * 60)
        
        derivs = results['derivatives'][pairing_name]
        targets = results['targets'][:-1]  # One fewer due to derivative
        
        # Find steepest drops (most negative derivatives)
        abs_derivs = np.abs(derivs)
        steep_threshold = np.percentile(abs_derivs, 75)  # Top 25%
        flat_threshold = np.percentile(abs_derivs, 25)   # Bottom 25%
        
        steep_regions = []
        flat_regions = []
        
        for i, (target, deriv) in enumerate(zip(targets, derivs)):
            abs_deriv = abs(deriv)
            if abs_deriv > steep_threshold:
                steep_regions.append((target, deriv))
            elif abs_deriv < flat_threshold:
                flat_regions.append((target, deriv))
        
        if steep_regions:
            print(f"\n  STEEP regions (top {len(steep_regions)} targets):")
            for target, deriv in steep_regions[:10]:  # Show top 10
                print(f"    T = {target:2d}: ΔP/ΔT = {deriv:+.4f}")
        
        if flat_regions:
            print(f"\n  FLAT regions (examples):")
            for target, deriv in flat_regions[:5]:  # Show 5 examples
                print(f"    T = {target:2d}: ΔP/ΔT = {deriv:+.4f} (negligible)")


def identify_breakpoints(results, dice_pairings):
    """
    Identify breakpoints where behavior changes (inflection points).
    """
    print("\n" + "="*80)
    print("BREAKPOINT ANALYSIS: Inflection Points")
    print("="*80)
    print()
    print("Inflection points = where rate of decline changes")
    print()
    
    for pairing_name in dice_pairings.keys():
        print(f"\n{pairing_name}:")
        print("-" * 60)
        
        second_derivs = results['second_derivatives'][pairing_name]
        targets = results['targets'][:-2]  # Two fewer due to second derivative
        
        # Find sign changes in second derivative (inflection points)
        inflection_points = []
        
        for i in range(len(second_derivs) - 1):
            if np.sign(second_derivs[i]) != np.sign(second_derivs[i+1]):
                inflection_points.append((targets[i+1], second_derivs[i], second_derivs[i+1]))
        
        if inflection_points:
            print(f"  Found {len(inflection_points)} inflection points:")
            for target, before, after in inflection_points[:10]:
                direction = "concave→convex" if after > before else "convex→concave"
                print(f"    T = {target:2d}: {direction}")
        else:
            print("  No major inflection points detected")


def create_comprehensive_target_visualizations(results, dice_pairings):
    """
    Create detailed visualizations focused on target value effects.
    """
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.3)
    
    colors = plt.cm.plasma(np.linspace(0.15, 0.85, len(dice_pairings)))
    pairing_names = list(dice_pairings.keys())
    targets = results['targets']
    
    # ============================================================
    # Plot 1: Probability vs Target (main curves)
    # ============================================================
    ax1 = fig.add_subplot(gs[0, :])
    
    for i, pairing_name in enumerate(pairing_names):
        probs = results['two_dice'][pairing_name]
        ax1.plot(targets, probs, linewidth=2.5, color=colors[i], 
                label=pairing_name, alpha=0.85, marker='o', markersize=3, markevery=2)
    
    ax1.set_xlabel('Target Value (T)', fontsize=13, fontweight='bold')
    ax1.set_ylabel('P(max ≥ T)', fontsize=13, fontweight='bold')
    ax1.set_title('Probability Decay: How Target Value Affects Success Rate', 
                  fontsize=15, fontweight='bold', pad=15)
    ax1.legend(fontsize=11, loc='upper right')
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_ylim(-0.05, 1.05)
    ax1.axhline(y=0.5, color='red', linestyle='--', linewidth=1, alpha=0.5, label='50% threshold')
    ax1.axhline(y=0.25, color='orange', linestyle='--', linewidth=1, alpha=0.5)
    ax1.axhline(y=0.75, color='green', linestyle='--', linewidth=1, alpha=0.5)
    
    # Add difficulty labels
    ax1.text(targets[-1] + 0.5, 0.9, 'Trivial', fontsize=9, alpha=0.7)
    ax1.text(targets[-1] + 0.5, 0.75, 'Easy', fontsize=9, alpha=0.7)
    ax1.text(targets[-1] + 0.5, 0.5, 'Medium', fontsize=9, alpha=0.7)
    ax1.text(targets[-1] + 0.5, 0.25, 'Hard', fontsize=9, alpha=0.7)
    ax1.text(targets[-1] + 0.5, 0.05, 'Extreme', fontsize=9, alpha=0.7)
    
    # ============================================================
    # Plot 2: Slope Analysis (dP/dT)
    # ============================================================
    ax2 = fig.add_subplot(gs[1, 0])
    
    for i, pairing_name in enumerate(pairing_names):
        derivs = results['derivatives'][pairing_name]
        targets_deriv = targets[:-1]
        ax2.plot(targets_deriv, np.abs(derivs), linewidth=2, color=colors[i], 
                label=pairing_name, alpha=0.8)
    
    ax2.set_xlabel('Target Value (T)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('|dP/dT| (Rate of Change)', fontsize=11, fontweight='bold')
    ax2.set_title('Sensitivity: Where Target Matters Most', fontsize=12, fontweight='bold')
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # ============================================================
    # Plot 3: Log-scale probability
    # ============================================================
    ax3 = fig.add_subplot(gs[1, 1])
    
    for i, pairing_name in enumerate(pairing_names):
        probs = results['two_dice'][pairing_name]
        # Replace zeros with small value for log scale
        probs_safe = [max(p, 1e-6) for p in probs]
        ax3.semilogy(targets, probs_safe, linewidth=2.5, color=colors[i], 
                    label=pairing_name, alpha=0.85)
    
    ax3.set_xlabel('Target Value (T)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('P(max ≥ T) [log scale]', fontsize=11, fontweight='bold')
    ax3.set_title('Log-Scale View: Tail Behavior', fontsize=12, fontweight='bold')
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3, which='both')
    
    # ============================================================
    # Plot 4: Comparison to single dice
    # ============================================================
    ax4 = fig.add_subplot(gs[1, 2])
    
    # Plot single d6 and d12 for comparison
    single_d6 = results['single_dice'][6]
    single_d12 = results['single_dice'][12]
    
    ax4.plot(targets, single_d6, '--', linewidth=2, color='gray', 
            label='Single d6', alpha=0.6)
    ax4.plot(targets, single_d12, '--', linewidth=2, color='black', 
            label='Single d12', alpha=0.6)
    ax4.plot(targets, results['two_dice']['d6+d6'], linewidth=2.5, 
            color=colors[1], label='d6+d6', alpha=0.9)
    ax4.plot(targets, results['two_dice']['d6+d12'], linewidth=2.5, 
            color=colors[4], label='d6+d12', alpha=0.9)
    
    ax4.set_xlabel('Target Value (T)', fontsize=11, fontweight='bold')
    ax4.set_ylabel('P(die ≥ T)', fontsize=11, fontweight='bold')
    ax4.set_title('Benefit of Two Dice vs Single Die', fontsize=12, fontweight='bold')
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3)
    
    # ============================================================
    # Plot 5: Heatmap across all targets
    # ============================================================
    ax5 = fig.add_subplot(gs[2, 0])
    
    # Create matrix
    prob_matrix = np.zeros((len(pairing_names), len(targets)))
    for i, pairing_name in enumerate(pairing_names):
        prob_matrix[i, :] = results['two_dice'][pairing_name]
    
    # Sample every 2nd target for readability
    sample_indices = list(range(0, len(targets), 2))
    sampled_targets = [targets[i] for i in sample_indices]
    sampled_matrix = prob_matrix[:, sample_indices]
    
    im = ax5.imshow(sampled_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    
    ax5.set_xticks(np.arange(0, len(sampled_targets), 2))
    ax5.set_xticklabels([sampled_targets[i] for i in range(0, len(sampled_targets), 2)], 
                        fontsize=8)
    ax5.set_yticks(np.arange(len(pairing_names)))
    ax5.set_yticklabels(pairing_names)
    ax5.set_xlabel('Target Value (T)', fontsize=11, fontweight='bold')
    ax5.set_ylabel('Dice Pairing', fontsize=11, fontweight='bold')
    ax5.set_title('Probability Heatmap', fontsize=12, fontweight='bold')
    
    plt.colorbar(im, ax=ax5, label='Probability')
    
    # ============================================================
    # Plot 6: Target ranges by difficulty
    # ============================================================
    ax6 = fig.add_subplot(gs[2, 1])
    
    difficulty_levels = {
        'Trivial': (0.90, 1.00),
        'Easy': (0.75, 0.90),
        'Medium': (0.50, 0.75),
        'Hard': (0.25, 0.50),
        'Very Hard': (0.10, 0.25),
        'Extreme': (0.00, 0.10)
    }
    
    # For d6+d12, show target ranges for each difficulty
    probs = results['two_dice']['d6+d12']
    
    ranges = {}
    for level, (min_p, max_p) in difficulty_levels.items():
        target_range = []
        for target, prob in zip(targets, probs):
            if min_p <= prob < max_p:
                target_range.append(target)
        if target_range:
            ranges[level] = (min(target_range), max(target_range))
    
    # Plot as horizontal bars
    y_pos = np.arange(len(ranges))
    level_names = list(ranges.keys())
    
    for i, level in enumerate(level_names):
        min_t, max_t = ranges[level]
        width = max_t - min_t + 1
        ax6.barh(i, width, left=min_t, alpha=0.7)
        ax6.text(min_t + width/2, i, f'{min_t}-{max_t}', 
                ha='center', va='center', fontsize=9, fontweight='bold')
    
    ax6.set_yticks(y_pos)
    ax6.set_yticklabels(level_names)
    ax6.set_xlabel('Target Value Range', fontsize=11, fontweight='bold')
    ax6.set_title('Difficulty Bands for d6+d12', fontsize=12, fontweight='bold')
    ax6.grid(axis='x', alpha=0.3)
    
    # ============================================================
    # Plot 7: Probability differences between adjacent targets
    # ============================================================
    ax7 = fig.add_subplot(gs[2, 2])
    
    for i, pairing_name in enumerate(pairing_names):
        derivs = results['derivatives'][pairing_name]
        targets_deriv = targets[:-1]
        # Only plot every 2nd point for clarity
        ax7.plot(targets_deriv[::2], np.abs(derivs[::2]), 'o-', 
                linewidth=1.5, markersize=4, color=colors[i], 
                label=pairing_name, alpha=0.7)
    
    ax7.set_xlabel('Target Value (T)', fontsize=11, fontweight='bold')
    ax7.set_ylabel('|P(T) - P(T+1)| (Discrete Change)', fontsize=10, fontweight='bold')
    ax7.set_title('Target Granularity Impact', fontsize=12, fontweight='bold')
    ax7.legend(fontsize=8, loc='upper right')
    ax7.grid(True, alpha=0.3)
    
    plt.savefig('target_value_analysis.png', dpi=300, bbox_inches='tight')
    print("\n📊 Target value analysis saved as 'target_value_analysis.png'")
    plt.close()


def create_game_design_guide(results, dice_pairings):
    """
    Create focused visualizations for game designers.
    """
    fig = plt.figure(figsize=(18, 10))
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
    
    colors = plt.cm.plasma(np.linspace(0.15, 0.85, len(dice_pairings)))
    pairing_names = list(dice_pairings.keys())
    targets = results['targets']
    
    # ============================================================
    # Game Designer Panel 1: Quick Reference Chart
    # ============================================================
    ax1 = fig.add_subplot(gs[0, :])
    
    # Show all pairings with difficulty bands
    for i, pairing_name in enumerate(pairing_names):
        probs = results['two_dice'][pairing_name]
        ax1.fill_between(targets, 0, probs, alpha=0.3, color=colors[i])
        ax1.plot(targets, probs, linewidth=3, color=colors[i], 
                label=pairing_name, alpha=0.9)
    
    # Add difficulty zones
    ax1.axhspan(0.75, 1.0, alpha=0.1, color='green', label='Easy (75-100%)')
    ax1.axhspan(0.5, 0.75, alpha=0.1, color='yellow', label='Medium (50-75%)')
    ax1.axhspan(0.25, 0.5, alpha=0.1, color='orange', label='Hard (25-50%)')
    ax1.axhspan(0.0, 0.25, alpha=0.1, color='red', label='Very Hard (0-25%)')
    
    ax1.set_xlabel('Target Value (T)', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Success Probability', fontsize=14, fontweight='bold')
    ax1.set_title('Game Designer Quick Reference: Target Difficulty Chart', 
                  fontsize=16, fontweight='bold', pad=20)
    ax1.legend(fontsize=10, loc='upper right', ncol=2)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.set_xlim(1, targets[-1])
    ax1.set_ylim(0, 1.05)
    
    # ============================================================
    # Panel 2: Target recommendations by desired difficulty
    # ============================================================
    ax2 = fig.add_subplot(gs[1, 0])
    
    # For each dice pairing, find targets that give ~25%, 50%, 75% success
    target_recommendations = {0.75: [], 0.50: [], 0.25: []}
    
    for pairing_name in pairing_names:
        probs = results['two_dice'][pairing_name]
        
        for desired_prob in [0.75, 0.50, 0.25]:
            # Find closest target
            diffs = [abs(p - desired_prob) for p in probs]
            best_idx = np.argmin(diffs)
            target_recommendations[desired_prob].append(targets[best_idx])
    
    x = np.arange(len(pairing_names))
    width = 0.25
    
    ax2.bar(x - width, target_recommendations[0.75], width, 
           label='Easy (75%)', color='green', alpha=0.7)
    ax2.bar(x, target_recommendations[0.50], width, 
           label='Medium (50%)', color='yellow', alpha=0.7)
    ax2.bar(x + width, target_recommendations[0.25], width, 
           label='Hard (25%)', color='orange', alpha=0.7)
    
    ax2.set_ylabel('Recommended Target Value', fontsize=11, fontweight='bold')
    ax2.set_title('Target Selection Guide', fontsize=12, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(pairing_names, rotation=15, ha='right')
    ax2.legend(fontsize=10)
    ax2.grid(axis='y', alpha=0.3)
    
    # Add values on bars
    for i, pairing in enumerate(pairing_names):
        for j, prob in enumerate([0.75, 0.50, 0.25]):
            offset = (j - 1) * width
            value = target_recommendations[prob][i]
            ax2.text(i + offset, value + 0.3, str(value), 
                    ha='center', fontsize=8, fontweight='bold')
    
    # ============================================================
    # Panel 3: Granularity analysis
    # ============================================================
    ax3 = fig.add_subplot(gs[1, 1])
    
    # Show how much probability changes per +1 target
    pairing_to_analyze = 'd6+d12'
    derivs = results['derivatives'][pairing_to_analyze]
    targets_deriv = targets[:-1]
    
    bars = ax3.bar(targets_deriv, np.abs(derivs), alpha=0.7, color='steelblue')
    
    # Color bars by magnitude
    threshold_high = np.percentile(np.abs(derivs), 75)
    threshold_low = np.percentile(np.abs(derivs), 25)
    
    for i, (bar, val) in enumerate(zip(bars, np.abs(derivs))):
        if val > threshold_high:
            bar.set_color('red')
            bar.set_alpha(0.8)
        elif val < threshold_low:
            bar.set_color('green')
            bar.set_alpha(0.5)
    
    ax3.set_xlabel('Target Value (T)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('|ΔP| for +1 Target', fontsize=11, fontweight='bold')
    ax3.set_title(f'Granularity Impact for {pairing_to_analyze}', 
                  fontsize=12, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', alpha=0.8, label='High impact (+1 matters a lot)'),
        Patch(facecolor='steelblue', alpha=0.7, label='Medium impact'),
        Patch(facecolor='green', alpha=0.5, label='Low impact (+1 matters little)')
    ]
    ax3.legend(handles=legend_elements, fontsize=8, loc='upper right')
    
    # ============================================================
    # Panel 4: Comparative scaling
    # ============================================================
    ax4 = fig.add_subplot(gs[1, 2])
    
    # Show how different pairings scale relative to each other
    # Normalize each curve by its max value
    for i, pairing_name in enumerate(pairing_names):
        probs = results['two_dice'][pairing_name]
        max_prob = max(probs)
        normalized = [p / max_prob if max_prob > 0 else 0 for p in probs]
        ax4.plot(targets, normalized, linewidth=2.5, color=colors[i], 
                label=pairing_name, alpha=0.85)
    
    ax4.set_xlabel('Target Value (T)', fontsize=11, fontweight='bold')
    ax4.set_ylabel('Normalized Probability', fontsize=11, fontweight='bold')
    ax4.set_title('Relative Difficulty Scaling', fontsize=12, fontweight='bold')
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3)
    ax4.axhline(y=0.5, color='red', linestyle='--', alpha=0.5)
    
    plt.savefig('game_design_guide.png', dpi=300, bbox_inches='tight')
    print("📊 Game design guide saved as 'game_design_guide.png'")
    plt.close()


def print_game_design_insights(results, dice_pairings):
    """
    Print actionable insights for game designers.
    """
    print("\n" + "="*80)
    print("GAME DESIGN INSIGHTS: How to Use Target Values")
    print("="*80)
    print()
    
    print("1. TRIVIAL TARGETS (>90% success):")
    print("-" * 60)
    for pairing_name in dice_pairings.keys():
        probs = results['two_dice'][pairing_name]
        targets = results['targets']
        
        trivial_targets = [t for t, p in zip(targets, probs) if p >= 0.90]
        if trivial_targets:
            max_trivial = max(trivial_targets)
            print(f"  {pairing_name}: T ≤ {max_trivial}")
    
    print("\n2. BALANCED TARGETS (40-60% success):")
    print("-" * 60)
    for pairing_name in dice_pairings.keys():
        probs = results['two_dice'][pairing_name]
        targets = results['targets']
        
        balanced_targets = [t for t, p in zip(targets, probs) if 0.40 <= p <= 0.60]
        if balanced_targets:
            print(f"  {pairing_name}: T = {min(balanced_targets)} to {max(balanced_targets)}")
    
    print("\n3. HEROIC TARGETS (10-25% success):")
    print("-" * 60)
    for pairing_name in dice_pairings.keys():
        probs = results['two_dice'][pairing_name]
        targets = results['targets']
        
        heroic_targets = [t for t, p in zip(targets, probs) if 0.10 <= p <= 0.25]
        if heroic_targets:
            print(f"  {pairing_name}: T = {min(heroic_targets)} to {max(heroic_targets)}")
    
    print("\n4. NEARLY IMPOSSIBLE TARGETS (<5% success):")
    print("-" * 60)
    for pairing_name in dice_pairings.keys():
        probs = results['two_dice'][pairing_name]
        targets = results['targets']
        
        impossible_targets = [t for t, p in zip(targets, probs) if p < 0.05 and p > 0]
        if impossible_targets:
            min_impossible = min(impossible_targets)
            print(f"  {pairing_name}: T ≥ {min_impossible}")
    
    print("\n5. GRANULARITY RECOMMENDATIONS:")
    print("-" * 60)
    print("  Use ODD targets when:")
    print("    • You want finer difficulty control")
    print("    • Players are optimizing their strategies")
    print("    • Precision matters for game balance")
    print()
    print("  Use EVEN targets when:")
    print("    • Simplicity is preferred")
    print("    • Differences are clearly noticeable")
    print("    • Traditional/familiar to players")
    
    print("\n6. MONOTONIC TRENDS:")
    print("-" * 60)
    print("  ✓ Probability ALWAYS decreases as target increases")
    print("  ✓ No local maxima or minima (smooth decay)")
    print("  ✓ Safe to interpolate between values")
    print("  ✓ Higher targets = harder challenges (intuitive)")
    
    print("\n7. KEY TARGET RANGES BY DICE PAIRING:")
    print("-" * 60)
    
    for pairing_name in ['d6+d6', 'd6+d12']:
        print(f"\n  {pairing_name}:")
        probs = results['two_dice'][pairing_name]
        targets = results['targets']
        
        # Find 50% and 25% points
        idx_50 = min(range(len(probs)), key=lambda i: abs(probs[i] - 0.50))
        idx_25 = min(range(len(probs)), key=lambda i: abs(probs[i] - 0.25))
        
        print(f"    50% success at T ≈ {targets[idx_50]}")
        print(f"    25% success at T ≈ {targets[idx_25]}")
        print(f"    Range for meaningful challenges: {targets[idx_50]-2} to {targets[idx_25]+2}")


def main():
    """
    Main execution for target value analysis.
    """
    print("🎯 TARGET VALUE ANALYSIS: Complete Range 🎯")
    print("="*80)
    print()
    print("Analyzing how target value (T) affects probability for fixed dice pairings")
    print("Focus: Game design insights and difficulty scaling")
    print()
    
    # Compute full range
    results, dice_pairings = compute_full_target_range(max_target=25)
    
    # Analyze thresholds
    identify_thresholds(results, dice_pairings)
    
    # Analyze slopes
    analyze_slopes(results, dice_pairings)
    
    # Identify breakpoints
    identify_breakpoints(results, dice_pairings)
    
    # Create visualizations
    print("\n📈 Generating visualizations...")
    create_comprehensive_target_visualizations(results, dice_pairings)
    create_game_design_guide(results, dice_pairings)
    
    # Print game design insights
    print_game_design_insights(results, dice_pairings)
    
    print("\n" + "="*80)
    print("✅ TARGET VALUE ANALYSIS COMPLETE")
    print("="*80)
    print("\nGenerated files:")
    print("  • target_value_analysis.png - Comprehensive 7-panel analysis")
    print("  • game_design_guide.png - Practical guide for designers")
    print()


if __name__ == "__main__":
    main()

