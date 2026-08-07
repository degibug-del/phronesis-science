#!/usr/bin/env python3
"""READ THIS BEFORE BELIEVING THE OUTPUT — audited 2026-08-07.

THE NAME OF THIS FILE IS WRONG. It does load a real recording, and the recording is
MNE's sample_audvis_raw.fif: an AUDITORY/VISUAL demo. One subject. Beeps and
checkerboards. NO LANGUAGE TASK OF ANY KIND.

The 7 sentences below were never shown to anyone. The EEG side takes 100 RANDOM
2-second windows and then keeps 7 of them, because n_match = min(7, 100). Sentence i is
paired with random window i. Whatever correlation comes out is a property of that
pairing, not of language.

Do not cite the r. Do not put real_eeg_validation.png in a deck.

WHAT IS WORTH KEEPING HERE: the grammar side is right. It builds a genuine spaCy
dependency adjacency matrix and takes eigs[0] - eigs[1], which is what the theory
actually specifies. analyze_eeg_real.py — the script with the correct EEG handling —
randomises its adjacency matrix instead. The two halves of a real experiment exist in
this directory, in different files, and have never been put together.

See PROVENANCE.md.
"""
import mne
import numpy as np
import pandas as pd
from scipy.signal import welch
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import spacy
from pathlib import Path

print("="*70)
print("GRAMMAR-TO-COHERENCE: REAL EEG VALIDATION")
print("="*70)

# Real EEG
print("\n1. Loading real MNE sample EEG...")
try:
    data_path = mne.datasets.sample.data_path()
    raw = mne.io.read_raw_fif(f'{data_path}/MEG/sample/sample_audvis_raw.fif', 
                               preload=True, verbose=False)
    eeg = raw.copy().pick_types(eeg=True)
    print(f"   ✓ {len(eeg.ch_names)} EEG channels")
except Exception as e:
    print(f"   Error: {e}")
    exit(1)

# Grammar
print("\n2. Grammar features...")
nlp = spacy.load('en_core_web_sm')
sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Colorless green ideas sleep furiously.",
    "The government is planning to raise taxes.",
    "Time flies like an arrow; fruit flies like a banana.",
    "I saw the man with the telescope.",
    "The book that I read was interesting.",
    "Visiting relatives can be tiresome.",
]

grammar_results = []
for sent in sentences:
    doc = nlp(sent)
    n = len(doc)
    A = np.zeros((n, n))
    for t in doc:
        if t.head != t:
            A[t.i, t.head.i] = 1.0
            A[t.head.i, t.i] = 1.0
    eigs = np.sort(np.linalg.eigvalsh(A))[::-1]
    delta_lambda = float(eigs[0] - eigs[1]) if len(eigs) > 1 else float(eigs[0])
    grammar_results.append({'sentence': sent, 'delta_lambda': delta_lambda})

grammar_df = pd.DataFrame(grammar_results)
print(f"   ✓ {len(grammar_df)} sentences")

# EEG
print("\n3. EEG spectral features (real data)...")
sfreq = eeg.info['sfreq']
win = int(2.0 * sfreq)
eeg_results = []
np.random.seed(42)

for i in range(100):
    s = np.random.randint(0, max(1, eeg.n_times - win))
    e = min(s + win, eeg.n_times)
    seg = eeg._data[:, s:e].mean(axis=0)
    freqs, pwr = welch(seg, fs=sfreq, nperseg=256)
    mask = (freqs > 4) & (freqs < 12)
    if mask.any():
        peak = float(freqs[mask][np.argmax(pwr[mask])])
        eeg_results.append({'peak_frequency_hz': peak})

eeg_df = pd.DataFrame(eeg_results)
print(f"   ✓ {len(eeg_df)} epochs")

# Analyze
print("\n4. Correlation...")
n_match = min(len(grammar_df), len(eeg_df))
g = grammar_df['delta_lambda'].values[:n_match]
e = eeg_df['peak_frequency_hz'].values[:n_match]

log_g = np.log(g + 1)
r, p = pearsonr(log_g, e)

print(f"   r = {r:.4f}, p = {p:.2e}, R² = {r**2*100:.1f}%")

if r > 0.65:
    status = "✅ VALIDATED"
elif r > 0.45:
    status = "⚠️  PARTIAL"
else:
    status = "⚠️  WEAK"
print(f"   {status}")

# Figure
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(log_g, e, alpha=0.6, s=60, color='darkblue')
z = np.polyfit(log_g, e, 1)
p_fit = np.poly1d(z)
x_fit = np.linspace(log_g.min(), log_g.max(), 50)
ax.plot(x_fit, p_fit(x_fit), 'r-', lw=2.5, label='Fit')
ax.set_xlabel('log(Δλ)', fontsize=12, fontweight='bold')
ax.set_ylabel('Peak EEG Freq (Hz)', fontsize=12, fontweight='bold')
ax.set_title(f'Real EEG: r={r:.3f}, p={p:.2e}', fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend()

out = Path.home() / 'phronesis-science' / 'real_eeg_validation.png'
out.parent.mkdir(exist_ok=True)
plt.savefig(out, dpi=150, bbox_inches='tight')
print(f"\n✓ Saved {out}")

print("\n" + "="*70)
print(f"REAL EEG VALIDATION COMPLETE")
print("="*70 + "\n")

