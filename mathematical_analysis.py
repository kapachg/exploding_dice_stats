"""
Mathematical Analysis of Die Size vs Target Threshold Relationship

This module provides formal mathematical characterization of how the second die size
affects P(max(X,Y) >= T) under exploding dice mechanics.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from exploding_dice import ExplodingDie, probability_max_of_two


def formal_probability_expression():
    """
    Document the formal mathematical expression for P(max(X,Y) >= T).
    """
    print("="*80)
    print("FORMAL MATHEMATICAL EXPRESSION")
    print("="*80)
    print()
    print("For two independent exploding dice X ~ d6 and Y ~ dN:")
    print()
    print("P(max(X,Y) ≥ T) = 1 - P(max(X,Y) < T)")
    print("                = 1 - P(X < T AND Y < T)")
    print("                = 1 - P(X < T) · P(Y < T)    [by independence]")
    print("                = 1 - F_X(T-1) · F_Y(T-1)")
    print()
    print("Where F_X and F_Y are the cumulative distribution functions (CDFs).")
    print()
    print("Equivalently, using the complementary CDF (survival function):")
    print()
    print("P(max(X,Y) ≥ T) = 1 - [1 - S_X(T)] · [1 - S_Y(T)]")
    print()
    print("Where S_X(T) = P(X ≥ T) and S_Y(T) = P(Y ≥ T)")
    print()
    print("This can be expanded as:")
    print()
    print("P(max(X,Y) ≥ T) = S_X(T) + S_Y(T) - S_X(T)·S_Y(T)")
    print()
    print("This reveals three components:")
    print("  1. S_X(T): Contribution from first die alone")
    print("  2. S_Y(T): Contribution from second die alone")
    print("  3. -S_X(T)·S_Y(T): Overlap correction (inclusion-exclusion)")
    print()
    print("="*80)
    print()


def compute_detailed_probabilities(targets=[4, 6, 8, 10]):
    """
    Compute probabilities with detailed breakdown for analysis.
    
    Returns:
        dict: Comprehensive probability data structure
    """
    d6 = ExplodingDie(6)
    die_sizes = [4, 6, 8, 10, 12]
    
    # Also include fractional die sizes for smooth curves
    fine_die_sizes = np.linspace(4, 12, 50)
    
    results = {
        'discrete': {},
        'continuous': {},
        'components': {},
        'marginal': {},
        'targets': targets
    }
    
    # Discrete die sizes (actual dice)
    for target in targets:
        results['discrete'][target] = {}
        results['components'][target] = {}
        results['marginal'][target] = []
        
        s_x = d6.probability_at_least(target)  # Fixed d6 probability
        
        prev_prob = None
        for die_size in die_sizes:
            die = ExplodingDie(die_size)
            s_y = die.probability_at_least(target)
            prob_max = probability_max_of_two(d6, die, target)
            
            results['discrete'][target][die_size] = prob_max
            results['components'][target][die_size] = {
                'S_X': s_x,
                'S_Y': s_y,
                'overlap': s_x * s_y,
                'probability': prob_max
            }
            
            # Marginal improvement
            if prev_prob is not None:
                marginal = prob_max - prev_prob
                results['marginal'][target].append({
                    'from': prev_size,
                    'to': die_size,
                    'improvement': marginal,
                    'relative': marginal / prev_prob if prev_prob > 0 else 0
                })
            
            prev_prob = prob_max
            prev_size = die_size
    
    # Continuous approximation (for smooth curves)
    # We'll interpolate single-die probabilities
    for target in targets:
        results['continuous'][target] = {}
        
        # Get discrete points for interpolation
        discrete_sizes = []
        discrete_probs_y = []
        
        for die_size in die_sizes:
            die = ExplodingDie(die_size)
            discrete_sizes.append(die_size)
            discrete_probs_y.append(die.probability_at_least(target))
        
        # Interpolate
        continuous_probs = np.interp(fine_die_sizes, discrete_sizes, discrete_probs_y)
        
        s_x = d6.probability_at_least(target)
        
        for i, n in enumerate(fine_die_sizes):
            s_y = continuous_probs[i]
            prob_max = 1 - (1 - s_x) * (1 - s_y)
            results['continuous'][target][n] = prob_max
    
    return results, die_sizes, fine_die_sizes


def analyze_marginal_effects(results):
    """
    Analyze and print marginal effects and diminishing returns.
    """
    print("="*80)
    print("MARGINAL EFFECTS AND DIMINISHING RETURNS")
    print("="*80)
    print()
    
    for target in results['targets']:
        print(f"\nTarget ≥ {target}:")
        print("-" * 60)
        
        marginal_data = results['marginal'][target]
        
        for i, data in enumerate(marginal_data):
            improvement = data['improvement'] * 100
            relative = data['relative'] * 100
            
            print(f"  d{data['from']} → d{data['to']}: "
                  f"Δ = {improvement:+6.2f}pp  "
                  f"(relative: {relative:+5.1f}%)")
        
        # Identify pattern
        improvements = [d['improvement'] for d in marginal_data]
        
        if all(improvements[i] > improvements[i+1] for i in range(len(improvements)-1)):
            print("\n  Pattern: Consistent DIMINISHING RETURNS")
        elif all(improvements[i] < improvements[i+1] for i in range(len(improvements)-1)):
            print("\n  Pattern: INCREASING RETURNS (unusual!)")
        else:
            print("\n  Pattern: NON-MONOTONIC (complex interaction)")
            
            # Find peaks and troughs
            for i in range(1, len(improvements)-1):
                if improvements[i] > improvements[i-1] and improvements[i] > improvements[i+1]:
                    print(f"    → Peak improvement at d{marginal_data[i]['from']} → d{marginal_data[i]['to']}")
                elif improvements[i] < improvements[i-1] and improvements[i] < improvements[i+1]:
                    print(f"    → Trough (local minimum) at d{marginal_data[i]['from']} → d{marginal_data[i]['to']}")


def identify_threshold_effects(results, die_sizes):
    """
    Identify threshold effects and regime changes.
    """
    print("\n" + "="*80)
    print("THRESHOLD EFFECTS AND REGIME ANALYSIS")
    print("="*80)
    print()
    
    for target in results['targets']:
        print(f"\nTarget ≥ {target}:")
        print("-" * 60)
        
        # Analyze components
        components = results['components'][target]
        
        print("  Component Analysis:")
        for die_size in die_sizes:
            comp = components[die_size]
            s_x = comp['S_X']
            s_y = comp['S_Y']
            overlap = comp['overlap']
            
            # Which term dominates?
            contribution_x = s_x * (1 - s_y)  # Unique contribution from X
            contribution_y = s_y * (1 - s_x)  # Unique contribution from Y
            contribution_both = overlap
            
            print(f"\n    d6 + d{die_size}:")
            print(f"      S_X(d6) = {s_x:.4f}, S_Y(d{die_size}) = {s_y:.4f}")
            print(f"      Contribution from d6 only:     {contribution_x:.4f}")
            print(f"      Contribution from d{die_size} only:  {contribution_y:.4f}")
            print(f"      Overlap (both succeed):        {contribution_both:.4f}")
            
            if contribution_y > contribution_x * 2:
                print(f"      → d{die_size} DOMINATES (second die much stronger)")
            elif contribution_x > contribution_y * 2:
                print(f"      → d6 DOMINATES (first die much stronger)")
            else:
                print(f"      → BALANCED (both dice contribute significantly)")
        
        # Identify crossover points
        print("\n  Regime Analysis:")
        s_x = components[die_sizes[0]]['S_X']
        
        if s_x > 0.5:
            print(f"    d6 has HIGH base probability ({s_x:.1%})")
            print(f"    → Diminishing returns likely (ceiling effect)")
        elif s_x < 0.1:
            print(f"    d6 has LOW base probability ({s_x:.1%})")
            print(f"    → Large gains possible from second die")
        else:
            print(f"    d6 has MODERATE base probability ({s_x:.1%})")
            print(f"    → Balanced improvement potential")


def create_comprehensive_visualizations(results, die_sizes, fine_die_sizes):
    """
    Create detailed visualizations of the mathematical relationships.
    """
    targets = results['targets']
    
    # Create a large figure with multiple subplots
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(targets)))
    
    # ============================================================
    # Plot 1: Probability vs Die Size (main relationship)
    # ============================================================
    ax1 = fig.add_subplot(gs[0, :2])
    
    for i, target in enumerate(targets):
        # Plot continuous curve
        x_cont = list(results['continuous'][target].keys())
        y_cont = list(results['continuous'][target].values())
        ax1.plot(x_cont, y_cont, linewidth=2, color=colors[i], alpha=0.5, linestyle='-')
        
        # Plot discrete points
        x_disc = die_sizes
        y_disc = [results['discrete'][target][d] for d in die_sizes]
        ax1.plot(x_disc, y_disc, 'o', markersize=10, color=colors[i], 
                label=f'Target ≥{target}', linewidth=3, alpha=0.9)
    
    ax1.set_xlabel('Second Die Size (N)', fontsize=13, fontweight='bold')
    ax1.set_ylabel('P(max(d6, dN) ≥ Target)', fontsize=13, fontweight='bold')
    ax1.set_title('Probability as Function of Die Size', fontsize=14, fontweight='bold', pad=15)
    ax1.legend(fontsize=11, loc='best')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)
    ax1.set_xticks(die_sizes)
    ax1.set_xticklabels([f'd{d}' for d in die_sizes])
    
    # ============================================================
    # Plot 2: Marginal Improvement (derivative)
    # ============================================================
    ax2 = fig.add_subplot(gs[0, 2])
    
    width = 0.18
    x_positions = np.arange(len(die_sizes) - 1)
    
    for i, target in enumerate(targets):
        marginal_values = [d['improvement'] * 100 for d in results['marginal'][target]]
        offset = width * (i - len(targets)/2 + 0.5)
        ax2.bar(x_positions + offset, marginal_values, width, 
               label=f'≥{target}', color=colors[i], alpha=0.8)
    
    ax2.set_xlabel('Die Upgrade', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Marginal Gain (pp)', fontsize=11, fontweight='bold')
    ax2.set_title('Marginal Improvements', fontsize=12, fontweight='bold', pad=10)
    ax2.legend(fontsize=9)
    ax2.grid(axis='y', alpha=0.3)
    ax2.axhline(y=0, color='black', linewidth=1)
    ax2.set_xticks(x_positions)
    ax2.set_xticklabels([f'd{die_sizes[i]}→\nd{die_sizes[i+1]}' 
                         for i in range(len(die_sizes)-1)], fontsize=8)
    
    # ============================================================
    # Plot 3: Component Breakdown for Target ≥4
    # ============================================================
    ax3 = fig.add_subplot(gs[1, 0])
    
    target = 4
    x_pos = np.arange(len(die_sizes))
    
    s_x_vals = [results['components'][target][d]['S_X'] for d in die_sizes]
    s_y_vals = [results['components'][target][d]['S_Y'] for d in die_sizes]
    overlap_vals = [results['components'][target][d]['overlap'] for d in die_sizes]
    
    ax3.bar(x_pos, s_x_vals, width=0.25, label='S_X (d6)', alpha=0.8)
    ax3.bar(x_pos + 0.25, s_y_vals, width=0.25, label='S_Y (dN)', alpha=0.8)
    ax3.bar(x_pos + 0.5, overlap_vals, width=0.25, label='Overlap', alpha=0.8)
    
    ax3.set_xlabel('Second Die Size', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Probability', fontsize=11, fontweight='bold')
    ax3.set_title(f'Component Breakdown: Target ≥{target}', fontsize=12, fontweight='bold')
    ax3.legend(fontsize=9)
    ax3.set_xticks(x_pos + 0.25)
    ax3.set_xticklabels([f'd{d}' for d in die_sizes])
    ax3.grid(axis='y', alpha=0.3)
    
    # ============================================================
    # Plot 4: Component Breakdown for Target ≥10
    # ============================================================
    ax4 = fig.add_subplot(gs[1, 1])
    
    target = 10
    s_x_vals = [results['components'][target][d]['S_X'] for d in die_sizes]
    s_y_vals = [results['components'][target][d]['S_Y'] for d in die_sizes]
    overlap_vals = [results['components'][target][d]['overlap'] for d in die_sizes]
    
    ax4.bar(x_pos, s_x_vals, width=0.25, label='S_X (d6)', alpha=0.8)
    ax4.bar(x_pos + 0.25, s_y_vals, width=0.25, label='S_Y (dN)', alpha=0.8)
    ax4.bar(x_pos + 0.5, overlap_vals, width=0.25, label='Overlap', alpha=0.8)
    
    ax4.set_xlabel('Second Die Size', fontsize=11, fontweight='bold')
    ax4.set_ylabel('Probability', fontsize=11, fontweight='bold')
    ax4.set_title(f'Component Breakdown: Target ≥{target}', fontsize=12, fontweight='bold')
    ax4.legend(fontsize=9)
    ax4.set_xticks(x_pos + 0.25)
    ax4.set_xticklabels([f'd{d}' for d in die_sizes])
    ax4.grid(axis='y', alpha=0.3)
    
    # ============================================================
    # Plot 5: Relative Improvement Rate
    # ============================================================
    ax5 = fig.add_subplot(gs[1, 2])
    
    for i, target in enumerate(targets):
        relative_improvements = [d['relative'] * 100 for d in results['marginal'][target]]
        ax5.plot(range(len(relative_improvements)), relative_improvements, 
                'o-', markersize=8, linewidth=2, label=f'≥{target}', color=colors[i])
    
    ax5.set_xlabel('Upgrade Step', fontsize=11, fontweight='bold')
    ax5.set_ylabel('Relative Improvement (%)', fontsize=11, fontweight='bold')
    ax5.set_title('Relative Gain Rate', fontsize=12, fontweight='bold')
    ax5.legend(fontsize=9)
    ax5.grid(True, alpha=0.3)
    ax5.axhline(y=0, color='black', linewidth=1)
    ax5.set_xticks(range(len(die_sizes)-1))
    ax5.set_xticklabels([f'{i+1}' for i in range(len(die_sizes)-1)])
    
    # ============================================================
    # Plot 6: Second Derivative (acceleration of improvement)
    # ============================================================
    ax6 = fig.add_subplot(gs[2, 0])
    
    for i, target in enumerate(targets):
        marginal_values = [d['improvement'] for d in results['marginal'][target]]
        
        # Compute second differences (discrete second derivative)
        second_deriv = [marginal_values[j+1] - marginal_values[j] 
                       for j in range(len(marginal_values)-1)]
        
        ax6.plot(range(len(second_deriv)), [sd * 100 for sd in second_deriv], 
                'o-', markersize=8, linewidth=2, label=f'≥{target}', color=colors[i])
    
    ax6.set_xlabel('Upgrade Step', fontsize=11, fontweight='bold')
    ax6.set_ylabel('Acceleration (Δ²P, pp)', fontsize=11, fontweight='bold')
    ax6.set_title('Rate of Change in Marginal Gain', fontsize=12, fontweight='bold')
    ax6.legend(fontsize=9)
    ax6.grid(True, alpha=0.3)
    ax6.axhline(y=0, color='black', linewidth=1, linestyle='--')
    ax6.set_xticks(range(len(die_sizes)-2))
    ax6.set_xticklabels([f'{i+1}→{i+2}' for i in range(len(die_sizes)-2)], fontsize=8)
    
    # Add annotation
    ax6.text(0.5, 0.95, 'Positive = increasing returns\nNegative = diminishing returns',
            transform=ax6.transAxes, fontsize=8, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
    
    # ============================================================
    # Plot 7: Efficiency Frontier (probability per unit die size)
    # ============================================================
    ax7 = fig.add_subplot(gs[2, 1])
    
    for i, target in enumerate(targets):
        probabilities = [results['discrete'][target][d] for d in die_sizes]
        efficiency = [probabilities[j] / die_sizes[j] for j in range(len(die_sizes))]
        
        ax7.plot(die_sizes, efficiency, 'o-', markersize=8, linewidth=2, 
                label=f'≥{target}', color=colors[i])
    
    ax7.set_xlabel('Second Die Size', fontsize=11, fontweight='bold')
    ax7.set_ylabel('Probability / Die Size', fontsize=11, fontweight='bold')
    ax7.set_title('Efficiency Metric', fontsize=12, fontweight='bold')
    ax7.legend(fontsize=9)
    ax7.grid(True, alpha=0.3)
    ax7.set_xticks(die_sizes)
    ax7.set_xticklabels([f'd{d}' for d in die_sizes])
    
    # ============================================================
    # Plot 8: Heatmap of Probability Surface
    # ============================================================
    ax8 = fig.add_subplot(gs[2, 2])
    
    # Create probability matrix
    prob_matrix = np.zeros((len(targets), len(die_sizes)))
    for i, target in enumerate(targets):
        for j, die_size in enumerate(die_sizes):
            prob_matrix[i, j] = results['discrete'][target][die_size]
    
    im = ax8.imshow(prob_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    
    ax8.set_xticks(np.arange(len(die_sizes)))
    ax8.set_yticks(np.arange(len(targets)))
    ax8.set_xticklabels([f'd{d}' for d in die_sizes])
    ax8.set_yticklabels([f'≥{t}' for t in targets])
    ax8.set_xlabel('Second Die Size', fontsize=11, fontweight='bold')
    ax8.set_ylabel('Target Value', fontsize=11, fontweight='bold')
    ax8.set_title('Probability Heatmap', fontsize=12, fontweight='bold')
    
    # Add text annotations
    for i in range(len(targets)):
        for j in range(len(die_sizes)):
            text = ax8.text(j, i, f'{prob_matrix[i, j]:.2f}',
                          ha="center", va="center", color="black", fontsize=9)
    
    plt.colorbar(im, ax=ax8, label='Probability')
    
    plt.savefig('mathematical_analysis.png', dpi=300, bbox_inches='tight')
    print("\n📊 Comprehensive visualization saved as 'mathematical_analysis.png'")
    plt.close()


def create_3d_surface_plot(results, die_sizes, fine_die_sizes):
    """
    Create 3D surface plot showing probability as function of both die size and target.
    """
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    targets = results['targets']
    
    # Create mesh for surface
    N_mesh, T_mesh = np.meshgrid(fine_die_sizes, targets)
    P_mesh = np.zeros_like(N_mesh)
    
    for i, target in enumerate(targets):
        for j, n in enumerate(fine_die_sizes):
            P_mesh[i, j] = results['continuous'][target][n]
    
    # Plot surface
    surf = ax.plot_surface(N_mesh, T_mesh, P_mesh, cmap=cm.viridis, 
                          alpha=0.8, linewidth=0.5, edgecolor='black')
    
    # Plot discrete points
    for target in targets:
        for die_size in die_sizes:
            prob = results['discrete'][target][die_size]
            ax.scatter([die_size], [target], [prob], c='red', marker='o', s=50, alpha=1)
    
    ax.set_xlabel('Second Die Size (N)', fontsize=12, fontweight='bold', labelpad=10)
    ax.set_ylabel('Target Threshold (T)', fontsize=12, fontweight='bold', labelpad=10)
    ax.set_zlabel('P(max(d6, dN) ≥ T)', fontsize=12, fontweight='bold', labelpad=10)
    ax.set_title('Probability Surface: Die Size × Target Threshold', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add colorbar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    
    # Set viewing angle
    ax.view_init(elev=25, azim=135)
    
    plt.savefig('probability_surface_3d.png', dpi=300, bbox_inches='tight')
    print("📊 3D surface plot saved as 'probability_surface_3d.png'")
    plt.close()


def theoretical_analysis(results, die_sizes):
    """
    Provide theoretical analysis and insights.
    """
    print("\n" + "="*80)
    print("THEORETICAL INSIGHTS")
    print("="*80)
    print()
    
    print("1. LOW TARGET REGIME (T = 4):")
    print("-" * 60)
    target = 4
    print(f"   Base d6 probability: {results['components'][target][4]['S_X']:.1%}")
    print()
    print("   • d6 already has HIGH success rate (50%)")
    print("   • Ceiling effect: limited room for improvement")
    print("   • Marginal gains decrease consistently (diminishing returns)")
    print("   • Adding larger dice helps, but multiplicative factor is small")
    print()
    
    print("2. MEDIUM-LOW TARGET REGIME (T = 6):")
    print("-" * 60)
    target = 6
    print(f"   Base d6 probability: {results['components'][target][4]['S_X']:.1%}")
    print()
    print("   • d6 has MODERATE success rate (16.7%)")
    print("   • NON-MONOTONIC behavior observed!")
    print("   • d4's high explosion rate (25%) creates competitive advantage")
    print("   • Crossover effects between different die size ranges")
    print()
    
    print("3. MEDIUM-HIGH TARGET REGIME (T = 8):")
    print("-" * 60)
    target = 8
    print(f"   Base d6 probability: {results['components'][target][4]['S_X']:.1%}")
    print()
    print("   • d6 has LOW-MODERATE success rate (13.9%)")
    print("   • Large gains possible from bigger dice")
    print("   • d8 and d10 provide major jumps")
    print("   • Complex interaction patterns persist")
    print()
    
    print("4. HIGH TARGET REGIME (T = 10):")
    print("-" * 60)
    target = 10
    print(f"   Base d6 probability: {results['components'][target][4]['S_X']:.1%}")
    print()
    print("   • d6 has LOW success rate (8.3%)")
    print("   • Large relative improvements possible")
    print("   • d12 provides massive boost (+13.75pp vs d10)")
    print("   • Second die becomes DOMINANT factor")
    print()
    
    print("="*80)
    print("MATHEMATICAL STRUCTURE")
    print("="*80)
    print()
    print("The probability function P(N, T) = 1 - [1 - S_6(T)][1 - S_N(T)]")
    print("exhibits the following properties:")
    print()
    print("1. MONOTONICITY in N:")
    print("   ∂P/∂N = [1 - S_6(T)] · ∂S_N/∂N ≥ 0")
    print("   (always non-decreasing in continuous approximation)")
    print()
    print("2. CONCAVITY (diminishing returns):")
    print("   ∂²P/∂N² = [1 - S_6(T)] · ∂²S_N/∂N²")
    print("   Sign depends on ∂²S_N/∂N² (curvature of single-die CDF)")
    print()
    print("3. INTERACTION TERM:")
    print("   P(N,T) = S_6(T) + S_N(T) - S_6(T)·S_N(T)")
    print("   The negative interaction term creates complex dynamics")
    print()
    print("4. ASYMPTOTIC BEHAVIOR:")
    print("   As N → ∞: S_N(T) → 1 for fixed T")
    print("   Therefore: P(N,T) → 1 (guaranteed success)")
    print()
    print("5. DISCRETE JUMPS:")
    print("   Real dice (discrete N) create step functions")
    print("   Non-monotonic effects arise from explosion frequency jumps")
    print()


def main():
    """
    Main execution for mathematical analysis.
    """
    print("🔬 MATHEMATICAL ANALYSIS: DIE SIZE vs TARGET THRESHOLD 🔬")
    print("="*80)
    print()
    
    # Part 1: Formal expression
    formal_probability_expression()
    
    # Part 2: Compute detailed probabilities
    print("Computing detailed probability structures...")
    results, die_sizes, fine_die_sizes = compute_detailed_probabilities()
    print("✓ Computations complete\n")
    
    # Part 3: Marginal effects analysis
    analyze_marginal_effects(results)
    
    # Part 4: Threshold effects
    identify_threshold_effects(results, die_sizes)
    
    # Part 5: Theoretical analysis
    theoretical_analysis(results, die_sizes)
    
    # Part 6: Create visualizations
    print("\n📈 Generating comprehensive visualizations...")
    create_comprehensive_visualizations(results, die_sizes, fine_die_sizes)
    create_3d_surface_plot(results, die_sizes, fine_die_sizes)
    
    print("\n" + "="*80)
    print("✅ MATHEMATICAL ANALYSIS COMPLETE")
    print("="*80)
    print("\nGenerated files:")
    print("  • mathematical_analysis.png - 8-panel comprehensive analysis")
    print("  • probability_surface_3d.png - 3D surface plot")
    print()


if __name__ == "__main__":
    main()

