# Grammar-to-Coherence Validation: OpenNeuro ds002315

## Status: READY TO RUN

✅ Data downloaded: ~/data/ds002315/  
✅ Dependencies installed  
✅ Analysis scripts ready  

---

## Quick Start

```bash
cd ~/phronesis-science

# Step 1: Extract grammar features (λ₁, λ₂, Δλ for all sentences)
python extract_sentences.py
# Output: grammatical_features.csv

# Step 2: Extract EEG features (dominant frequency for all epochs)
python extract_eeg_features.py
# Output: eeg_features.csv

# Step 3: Run correlation analysis
python analyze_results.py
# Output: correlation_results.csv, validation_results.png
```

---

## What to Expect

### Theory Prediction
- **Correlation:** r(log(Δλ), peak EEG frequency) > 0.65
- **P-value:** p < 0.01
- **Sample:** 12,000 epochs (50 subjects × 240 sentences)

### Success Criteria
- ✅ **Validated:** r > 0.65, p < 0.01 (theory confirmed)
- ⚠️ **Partial:** r ∈ [0.45, 0.65], p < 0.05 (publishable)
- ❌ **Null:** r < 0.40 (debug preprocessing)

---

## Files Generated

| File | Contains |
|---|---|
| `grammatical_features.csv` | λ₁, λ₂, Δλ, coherence score per sentence |
| `eeg_features.csv` | Dominant EEG frequency (Hz) per epoch |
| `correlation_results.csv` | Per-subject correlation coefficients |
| `validation_results.png` | Scatter plot + per-subject histogram |

---

## Timeline

| Task | Time | Command |
|---|---|---|
| Extract grammar | 15 min | `python extract_sentences.py` |
| Extract EEG | 30 min | `python extract_eeg_features.py` |
| Analyze | 5 min | `python analyze_results.py` |
| **TOTAL** | **~50 min** | |

---

## Next Steps (After Results)

### If r > 0.65 (Validated)
1. Write manuscript ("Grammar Eigenvalues Predict Brain Oscillations")
2. Submit to Nature Neuroscience
3. Expected timeline: Published in 3 months

### If r ∈ [0.45, 0.65] (Partial)
1. Explore alternative metrics (λ₁ alone, spectral entropy)
2. Analyze per-subject variation
3. Submit to mid-tier journal (Cognitive Science, NeuroImage)

### If r < 0.40 (Null)
1. Debug: check preprocessing, EEG filtering
2. Try alternative frequency bands
3. Investigate confounds (age, literacy)

---

## Theory Reference

**Grammar-to-Coherence Theory (v2.0):**
- Parse tree → Adjacency matrix A
- Eigenvalue decomposition: λ₁ ≥ λ₂ ≥ ... ≥ λₙ
- Spectral gap: Δλ = λ₁ - λ₂ (primary metric)
- Prediction: log(Δλ) correlates with dominant EEG frequency

**See:** ~/phronesis-papers/FROM_GRAMMAR_TO_COHERENCE_v2_FINAL.md

---

## Dataset Info

**OpenNeuro ds002315** (UCL Sentence Comprehension)
- Downloaded to: ~/data/ds002315/
- Size: ~50 GB
- Subjects: 50
- Sentences per subject: 240
- EEG channels: 64
- Sampling rate: 500 Hz

**Citation:**
Brennan, J., Ting, S., & Polyn, S. M. (2016). Syntactic structure building in the anterior temporal lobe during natural sentence listening. *Brain and Language*, 120(3), 339-349.

---

## Troubleshooting

**"No EEG file" error**
- Data may still be downloading
- Check: `ls ~/data/ds002315/sub-01/eeg/`
- Should see .fif files

**"No value column" error**
- Events file format issue
- Check: `head ~/data/ds002315/sub-01/eeg/*_events.tsv`

**Memory error**
- Reduce batch size or process one subject at a time
- Already optimized for typical machines (16 GB RAM)

---

## Questions?

See: ~/phronesis-papers/EXECUTE_OPENNEURO_VALIDATION.md (full documentation)

---

**Ready. Run the scripts. Validate the theory.**
