#!/usr/bin/env python3
"""
Extract EEG features (dominant frequency) from ds002315
Outputs: eeg_features.csv
"""

import mne
import numpy as np
import pandas as pd
from scipy.signal import welch
from pathlib import Path

DATA_DIR = Path.home() / 'data' / 'ds002315'

if not DATA_DIR.exists():
    print(f"Error: {DATA_DIR} not found.")
    exit(1)

RESULTS = []

subject_dirs = sorted(DATA_DIR.glob('sub-*'))
print(f"Found {len(subject_dirs)} subjects")

for i, subject_dir in enumerate(subject_dirs):
    subject_id = subject_dir.name
    print(f"[{i+1}/{len(subject_dirs)}] {subject_id}...", end=' ', flush=True)

    # Find EEG file
    eeg_files = list(subject_dir.glob('eeg/*.fif'))
    if not eeg_files:
        print("No EEG file")
        continue

    eeg_file = eeg_files[0]

    try:
        # Load raw EEG
        raw = mne.io.read_raw_fif(str(eeg_file), preload=False, verbose=False)

        # Load events
        events_file = list(subject_dir.glob('eeg/*_events.tsv'))[0]
        events_df = pd.read_csv(events_file, sep='\t')

        # Get sentence-aligned events
        sentence_events = events_df[events_df['trial_type'] == 'stimulus'].reset_index(drop=True)

        epoch_count = 0
        for idx, event in sentence_events.iterrows():
            t_start = int(event['onset'] * raw.info['sfreq'])
            t_end = t_start + int(2.0 * raw.info['sfreq'])  # 2 sec window

            if t_end > raw.n_times:
                continue

            try:
                # Extract EEG segment (all channels, mean across channels)
                eeg_segment = raw[:, t_start:t_end][0]
                eeg_mean = eeg_segment.mean(axis=0)

                # Compute spectral peak (Welch method)
                freqs, power = welch(eeg_mean,
                                    fs=raw.info['sfreq'],
                                    nperseg=256)

                # Find peak in 4-12 Hz (theta/alpha)
                mask = (freqs > 4) & (freqs < 12)
                if mask.any():
                    peak_freq = float(freqs[mask][np.argmax(power[mask])])
                else:
                    peak_freq = np.nan

                RESULTS.append({
                    'subject': subject_id,
                    'event_idx': int(idx),
                    'peak_frequency_hz': peak_freq
                })

                epoch_count += 1
            except Exception as e:
                continue

        print(f"{epoch_count} epochs")

    except Exception as e:
        print(f"Error: {e}")
        continue

# Save
if RESULTS:
    eeg_df = pd.DataFrame(RESULTS)
    eeg_df.to_csv('eeg_features.csv', index=False)
    print(f"\n✓ Extracted {len(eeg_df)} EEG epochs")
    print(f"  Saved to: eeg_features.csv")
else:
    print("No EEG features extracted.")
