#!/usr/bin/env python3
"""
Extract grammatical features (eigenvalues) from ds002315 sentences
Outputs: grammatical_features.csv
"""

import os
import pandas as pd
import spacy
import numpy as np
from pathlib import Path

# Load spaCy
nlp = spacy.load('en_core_web_sm')

# Dataset location
DATA_DIR = Path.home() / 'data' / 'ds002315'

if not DATA_DIR.exists():
    print(f"Error: {DATA_DIR} not found. Download ds002315 first.")
    exit(1)

# Results storage
RESULTS = []

# For each subject
subject_dirs = sorted(DATA_DIR.glob('sub-*'))
print(f"Found {len(subject_dirs)} subjects")

for i, subject_dir in enumerate(subject_dirs):
    subject_id = subject_dir.name
    print(f"[{i+1}/{len(subject_dirs)}] {subject_id}...", end=' ', flush=True)

    # Find events file (contains sentence stimuli)
    events_files = list(subject_dir.glob('eeg/*_events.tsv'))
    if not events_files:
        print("No events file")
        continue

    events_file = events_files[0]
    events = pd.read_csv(events_file, sep='\t')

    # Extract sentences (value column contains stimulus text)
    if 'value' not in events.columns:
        print("No value column")
        continue

    sentences = events['value'].dropna().unique()
    sentence_count = 0

    for sentence in sentences:
        sentence = str(sentence).strip()
        if not sentence or len(sentence) < 3:
            continue

        try:
            # Parse with spaCy
            doc = nlp(sentence)
            n_words = len(doc)

            if n_words < 2:
                continue

            # Build adjacency matrix (dependency structure)
            A = np.zeros((n_words, n_words))
            for token in doc:
                if token.head != token:
                    A[token.i, token.head.i] = 1.0
                    A[token.head.i, token.i] = 1.0

            # Compute eigenvalues
            eigenvalues = np.linalg.eigvalsh(A)
            eigenvalues = np.sort(eigenvalues)[::-1]  # descending order

            lambda_1 = float(eigenvalues[0])
            lambda_2 = float(eigenvalues[1]) if len(eigenvalues) > 1 else 0.0
            delta_lambda = lambda_1 - lambda_2
            coherence = (delta_lambda / 3.0) * 100

            # Store result
            RESULTS.append({
                'subject': subject_id,
                'sentence': sentence,
                'n_words': n_words,
                'lambda_1': lambda_1,
                'lambda_2': lambda_2,
                'delta_lambda': delta_lambda,
                'coherence': coherence
            })

            sentence_count += 1
        except Exception as e:
            continue

    print(f"{sentence_count} sentences")

# Save to CSV
if RESULTS:
    results_df = pd.DataFrame(RESULTS)
    results_df.to_csv('grammatical_features.csv', index=False)
    print(f"\n✓ Extracted {len(results_df)} sentence-eigenvalue pairs")
    print(f"  Saved to: grammatical_features.csv")
else:
    print("No results extracted. Check data format.")
