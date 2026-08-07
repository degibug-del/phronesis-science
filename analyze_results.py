#!/usr/bin/env python3
"""
Correlation analysis: grammar eigenvalues vs EEG features
Outputs: correlation_results.csv, validation_results.png
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr
import matplotlib.pyplot as plt

# Load data
print("Loading data...", end=' ', flush=True)
try:
    grammar_df = pd.read_csv('grammatical_features.csv')
    eeg_df = pd.read_csv('eeg_features.csv')
    print("✓")
except FileNotFoundError as e:
    print(f"\nError: {e}")
    print("Run extract_sentences.py and extract_eeg_features.py first")
    exit(1)

print(f"Grammar features: {len(grammar_df)} rows")
print(f"EEG features: {len(eeg_df)} rows")

# Merge data by subject and event index
print("Merging data...", end=' ', flush=True)

# Reset indices to match row order
grammar_df['row_idx'] = range(len(grammar_df))
eeg_df['row_idx'] = range(len(eeg_df))

# Match by row (assuming same order)
n_match = min(len(grammar_df), len(eeg_df))
grammar_df = grammar_df.iloc[:n_match].reset_index(drop=True)
eeg_df = eeg_df.iloc[:n_match].reset_index(drop=True)

print(f"✓ Matched {n_match} rows")

# Extract variables
delta_lambda = grammar_df['delta_lambda'].values
peak_freq = eeg_df['peak_frequency_hz'].values

# Remove NaNs
valid = ~(np.isnan(delta_lambda) | np.isnan(peak_freq))
delta_lambda = delta_lambda[valid]
peak_freq = peak_freq[valid]

print(f"Valid epochs (no NaN): {len(delta_lambda)}")

# GROUP-LEVEL ANALYSIS
print("\nCORRELATION ANALYSIS")
print("="*60)

log_delta = np.log(delta_lambda + 1)
r_group, p_group = pearsonr(log_delta, peak_freq)
rho_group, p_spear = spearmanr(log_delta, peak_freq)

print(f"Group level ({len(delta_lambda)} epochs):")
print(f"  Pearson r: {r_group:.4f}")
print(f"  P-value: {p_group:.8f}")
print(f"  Spearman ρ: {rho_group:.4f}")
print(f"  R² (variance): {r_group**2:.4f} ({r_group**2*100:.1f}%)")

print(f"\nPrediction target: r > 0.65, p < 0.01")

if r_group > 0.65 and p_group < 0.01:
    status = "✅ VALIDATED"
elif r_group > 0.45 and p_group < 0.05:
    status = "⚠️  PARTIAL SUPPORT"
elif r_group > 0.30:
    status = "⚠️  WEAK SIGNAL"
else:
    status = "❌ NULL"

print(f"Status: {status}")

# PER-SUBJECT ANALYSIS
print(f"\nPer-subject analysis:")
results_list = []

for subject in grammar_df['subject'].unique():
    subj_mask = grammar_df['subject'] == subject
    subj_delta = delta_lambda[subj_mask.values[:len(delta_lambda)]]
    subj_freq = peak_freq[subj_mask.values[:len(peak_freq)]]

    if len(subj_delta) < 10:
        continue

    r, p = pearsonr(np.log(subj_delta + 1), subj_freq)
    results_list.append({
        'subject': subject,
        'n': len(subj_delta),
        'r': r,
        'p_value': p
    })

results_df = pd.DataFrame(results_list)
results_df.to_csv('correlation_results.csv', index=False)

print(f"  Subjects analyzed: {len(results_df)}")
print(f"  Mean r: {results_df['r'].mean():.4f}")
print(f"  Median r: {results_df['r'].median():.4f}")
print(f"  Range: [{results_df['r'].min():.4f}, {results_df['r'].max():.4f}]")
print(f"  Subjects r > 0.40: {(results_df['r'] > 0.40).sum()}/{len(results_df)}")

# FIGURES
print("\nGenerating figures...", end=' ', flush=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Panel 1: Scatter plot
ax1.scatter(log_delta, peak_freq, alpha=0.2, s=5, color='steelblue')
z = np.polyfit(log_delta, peak_freq, 1)
p_fit = np.poly1d(z)
x_fit = np.linspace(log_delta.min(), log_delta.max(), 100)
ax1.plot(x_fit, p_fit(x_fit), 'r-', linewidth=2.5, label=f'Linear fit')

ax1.set_xlabel('log(Δλ) [Grammar Spectral Gap]', fontsize=12, fontweight='bold')
ax1.set_ylabel('Dominant EEG Frequency (Hz)', fontsize=12, fontweight='bold')
ax1.set_title(f'Grammar-to-EEG Correlation\nr = {r_group:.4f}, p = {p_group:.2e}, n = {len(delta_lambda)}',
             fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_ylim([4, 12])

# Panel 2: Per-subject distribution
ax2.hist(results_df['r'], bins=15, edgecolor='black', alpha=0.7, color='steelblue')
ax2.axvline(results_df['r'].mean(), color='red', linestyle='--', linewidth=2.5,
           label=f'Mean r = {results_df["r"].mean():.3f}')
ax2.axvline(0.65, color='green', linestyle=':', linewidth=2.5, label='Target (r=0.65)')
ax2.set_xlabel('Per-Subject Correlation (r)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Count', fontsize=12, fontweight='bold')
ax2.set_title('Individual Subject Effects', fontsize=13, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3, axis='y', linestyle='--')

plt.tight_layout()
plt.savefig('validation_results.png', dpi=150, bbox_inches='tight')
print("✓")

print("\n" + "="*60)
print(f"Results saved:")
print(f"  - correlation_results.csv (per-subject correlations)")
print(f"  - validation_results.png (figures)")
print("="*60)
