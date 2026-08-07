# PROVENANCE — what the validation artifacts in this directory actually are

**Audited 2026-08-07.** Read this before citing any number in this directory, and before
any of it goes into a paper, a deck, a grant, or a repository.

## The finding, in one line

**No validation of the grammar-to-brain claim has ever been run on real data.** Every
artifact in this directory that looks like one is synthetic, unrelated to language, or
both — and two of them are labelled in ways that invite the opposite conclusion.

This is not an accusation of anything but ordinary drift. The scripts were written fast,
the honest ones say what they are in their own headers, and the misleading part is mostly
in the *file names and output labels* rather than the code. That is exactly why it needed
writing down: the code is honest and the artifacts are not, and people cite artifacts.

## Artifact by artifact

### `eeg_validation_results.json` — SYNTHETIC, labelled with a real dataset

```json
"dataset": "ds002315 (UCL Sentence Comprehension)",
"sample_size": 240, "correlation": 0.459, "p_value": 6.3e-14
```

Written by **`validate_synthetic.py`**, which is the only script in either directory using
this schema (`verdict`, `next_step`, `sample_size`). That script says plainly in its own
header: *"Generates realistic EEG and grammar features matching ds002315 structure."*
Matching the STRUCTURE of the dataset — not the dataset.

`ds002315` has never been downloaded on this machine:

```
~/data/ds002315               0 files
~/data/openneuro/ds002315     0 files (subject directories, all empty)
~/data/ds002315.tar.gz        993 bytes          a real EEG dataset is gigabytes
no .set / .fdt / .edf / .bdf / .fif anywhere under ~/data
```

**This is the one that propagated.** It is referenced from `phronesis-papers/READY_TO_SUBMIT.md`
and both MANUSCRIPT files cite a correlation. Anyone reading the JSON sees a real dataset
name, a plausible n, and a publishable p-value.

To its credit the file reports `"status": "WEAK SUPPORT"`, `"prediction_met": false` and
`"next_step": "DEBUG & REDESIGN"` — the synthetic result was not even flattering. The
problem is the dataset attribution, not the number.

### `correlation_results.csv` — SYNTHETIC

Eleven subjects, n=240 each, r between 0.48 and 0.57, p from 1e-15 to 1e-22. Also from
`validate_synthetic.py`, `np.random.seed(42)`. The uniformity across "subjects" is the tell:
real cross-subject EEG effects do not land in a 0.09-wide band.

### `validate_real_eeg.py` / `real_eeg_validation.png` — REAL DATA, WRONG DATA, n=7

The name is the problem. It does load a real recording — and the recording is
`sample_audvis_raw.fif`, MNE's **auditory/visual** demo: one subject, beeps and
checkerboards, **no language task of any kind**.

```python
sentences = [7 hand-picked sentences]        # never shown to anyone, ever
for i in range(100):
    s = np.random.randint(0, eeg.n_times - win)   # random 2-second windows
n_match = min(len(grammar_df), len(eeg_df))       # = 7
r, p = pearsonr(log_g, e)                         # 7 points
```

Seven sentences nobody read, paired by array index against seven randomly chosen windows
of an unrelated experiment. Whatever r comes out is a property of the pairing.

The one thing it gets right, and it is worth keeping: the grammar side uses a genuine spaCy
dependency parse and takes `eigs[0] - eigs[1]`. That is the correct construction, attached
to the wrong experiment.

### `analyze_eeg_real.py` — the right idea, never run, and randomises the grammar

This is the script that would do it properly: real BIDS layout, per-subject `.fif`, epochs
around sentence events. It has never run, because the data is not there — and it fails
silently when that happens:

```python
if not eeg_file.exists():
    return None, None
```

It would also not have tested the thesis if it had run. The adjacency matrix is not parsed;
it is sequential edges plus **random** long-range edges seeded by the sentence's hash:

```python
np.random.seed(hash(sentence) % 2**32)
for _ in range(max(1, n_words // 3)):
    i, j = np.random.randint(0, n_words), np.random.randint(0, n_words)
```

Deterministic per sentence, so it looks stable across runs, but the "grammar" is noise with
a stable seed. `validate_real_eeg.py` already contains the real parse; this one needs it.

## What to do

1. **Do not cite `eeg_validation_results.json` or `correlation_results.csv` as evidence.**
   They are simulations. Both remain useful as pipeline tests.
2. **Treat `real_eeg_validation.png` as a plotting exercise.** It should not appear in a deck.
3. **Check what went to Zenodo.** The pitch deck cites DOI 10.5281/zenodo.21403447 and
   `MANUSCRIPT_ZENODO_SUBMISSION.md` exists. If a submitted manuscript attributes a
   correlation to ds002315, that is the one thing here that cannot be fixed locally.
4. **To actually run it:** download ds002315 for real, port the spaCy parse out of
   `validate_real_eeg.py` into `analyze_eeg_real.py` to replace the random edges, and run.
   Until then the claim is untested — which is different from false, and should be said
   that way.

## Why this happened, so it does not again

Every script here is honest about itself inside its own header. `validate_synthetic.py`
says it generates data in its first paragraph. The failure was entirely at the boundary:
outputs carried no provenance, so a JSON with `"dataset": "ds002315"` outlived the script
that wrote it and became evidence.

**An output file should say where it came from.** Each artifact now has a `.PROVENANCE.txt`
sidecar naming its generating script and whether the inputs were real.
