#!/usr/bin/env python3
"""Syntactic breakage detection — the one thing in ICM that measured up.

    python3 breakage.py --fit              refit the baseline from wellformed.txt
    python3 breakage.py "some text here"   score one string
    python3 breakage.py --eval             held-out operating characteristics

WHAT THIS IS

Six constructions of the Integrated Coherence Model were measured on 2026-08-07 and none
of them measures coherence. One thing did survive: the largest eigenvalue of a symmetric
dependency-parse adjacency matrix separates well-formed text from structurally broken text
at d = 1.63, while being completely blind to meaning — grammatical nonsense sits 0.004 away
from ordinary prose, p = 0.94.

So this answers "is this well-formed", not "is this any good". Named accordingly.

THE ENGINEERING PROBLEM, and it is the whole reason this file exists rather than a
one-line export of lambda1: LAMBDA1 GROWS WITH LENGTH. The first dissociation run failed
entirely because of it — unmatched stimuli put the two short conditions at the two lowest
lambda1 and the design measured word count. The paired shuffle test worked only because a
shuffle holds length fixed by construction.

A product cannot hold length fixed. It gets whatever text it is given. So a raw lambda1
threshold is useless across texts, and the fix is to score against what lambda1 SHOULD be
for a well-formed text of that length:

    z = (lambda1 - predicted(n)) / residual_sd

predicted(n) is fitted on ordinary prose. A z near zero means "as hub-like as well-formed
text this long"; a large positive z means the parse is flatter and starrier than it should
be, which is what breakage looks like.

HONEST LIMITS, stated because they bound every number below:

  · The baseline corpus is 296 sentences from this project's own papers. It is real
    well-formed English and it is ONE register, written by two authors. A detector
    calibrated on technical prose should be expected to drift on dialogue, poetry, or
    transcripts, and nothing here has tested that.
  · Evaluation is on held-out sentences from the same corpus, so it measures whether the
    length model generalises, not whether the register does.
  · The negative class is agrammatical text and word shuffles, both constructed. Real
    broken text — OCR, ASR output, translationese, a child's writing — is not represented.

═══════════════════════════════════════════════════════════════════════════════════════
IT DOES NOT WORK. Measured 2026-08-07, the same day it was built. Kept as the record.

The detector was the survivor of six failed constructions — lambda1 separating a sentence
from its own shuffle 11 times out of 12, blind to meaning, large effect on agrammatical
text. Building it properly meant calibrating out length, and calibrating out length meant
getting a real corpus, and the real corpus killed it.

    corpus                        original > shuffled    mean Δλ1
    12 sentences written for the test     3 / 9            -0.047
    89 held out from this project's papers 75 / 13         +0.228

THE EFFECT REVERSES. On text somebody wrote for another purpose, originals score HIGHER
than their shuffles — the opposite of the finding the whole line rested on. A measure whose
sign depends on which corpus you hand it is not a measure.

Held-out operating characteristics, for completeness:

    class                     mean z     AUC vs held-out well-formed
    well-formed (held out)      0.20      —
    shuffled                   -1.12      0.191      strongly anti-predictive
    agrammatical                0.39      0.586      chance

WHAT THIS RETROACTIVELY COSTS. The d = 1.63 dissociation was eight hand-written sentences
against eight others, written by the same person who wrote the prediction. Against 89
sentences he did not write, the agrammatical effect is chance. The confound experiment was
sound in design and its stimuli were too small and too homemade to carry the conclusion —
which is the criticism that was written INTO that file as the thing most worth replicating,
one experiment before it turned out to be the thing that mattered.

So the honest count is seven constructions and no instrument. The keyword engine in
phronesis-world/lib/icm.ts is what ICM is; the spectral line is closed.

The code stays runnable. `--eval` reproduces every number above, and if a larger or
differently-sourced corpus ever revives the effect, this is what it has to beat.
═══════════════════════════════════════════════════════════════════════════════════════
"""
import argparse
import json
import pathlib
import sys

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
CORPUS = HERE / 'wellformed.txt'
BASELINE = HERE / 'breakage-baseline.json'

_nlp = None


def nlp():
    global _nlp
    if _nlp is None:
        import spacy
        _nlp = spacy.load('en_core_web_sm')
    return _nlp


def lambda1(text):
    """Largest eigenvalue of the symmetric dependency adjacency matrix."""
    doc = nlp()(text)
    n = len(doc)
    if n < 2:
        return None, n
    A = np.zeros((n, n))
    for t in doc:
        if t.head.i != t.i:
            A[t.i, t.head.i] = A[t.head.i, t.i] = 1.0
    return float(np.sort(np.linalg.eigvalsh(A))[::-1][0]), n


def load_corpus():
    if not CORPUS.exists():
        sys.exit(f'no corpus at {CORPUS} — see the extraction note in the git history')
    return [s for s in CORPUS.read_text().split('\n') if s.strip()]


def fit(seed=7, holdout=0.3):
    """Fit predicted(n) on well-formed prose, holding a split back for evaluation.

    THE MODEL IS log(n), and it is chosen by comparison rather than by taste: a tree's
    lambda1 is bounded between sqrt(max degree) and max degree, and max degree grows
    sublinearly with length in real sentences. Linear, sqrt and log fits are all measured
    below and the best R^2 wins.
    """
    rows = []
    for s in load_corpus():
        l, n = lambda1(s)
        if l is not None and n >= 4:
            rows.append((n, l, s))
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(rows))
    cut = int(len(rows) * (1 - holdout))
    train = [rows[i] for i in idx[:cut]]
    test = [rows[i] for i in idx[cut:]]

    n_tr = np.array([r[0] for r in train], float)
    y_tr = np.array([r[1] for r in train], float)

    forms = {
        'linear': lambda n: n,
        'sqrt': np.sqrt,
        'log': np.log,
    }
    best = None
    for name, f in forms.items():
        x = f(n_tr)
        b = np.polyfit(x, y_tr, 1)
        pred = np.polyval(b, x)
        ss_res = float(((y_tr - pred) ** 2).sum())
        ss_tot = float(((y_tr - y_tr.mean()) ** 2).sum())
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
        if best is None or r2 > best['r2']:
            best = {'form': name, 'coef': [float(c) for c in b], 'r2': r2}
        print(f'    {name:<7} R² = {r2:.3f}')

    x = forms[best['form']](n_tr)
    resid = y_tr - np.polyval(best['coef'], x)
    best['sd'] = float(resid.std(ddof=1))
    best['n_train'] = len(train)
    best['n_test'] = len(test)
    best['seed'] = seed
    BASELINE.write_text(json.dumps(best, indent=2))
    return best, train, test


def _baseline():
    if not BASELINE.exists():
        sys.exit('no baseline — run: python3 breakage.py --fit')
    return json.loads(BASELINE.read_text())


def score(text, base=None):
    """z, and a band. Positive z means starrier than well-formed text of this length."""
    base = base or _baseline()
    l, n = lambda1(text)
    if l is None:
        return {'z': None, 'verdict': 'too short to say', 'lambda1': None, 'tokens': n}
    f = {'linear': lambda v: v, 'sqrt': np.sqrt, 'log': np.log}[base['form']]
    pred = float(np.polyval(base['coef'], f(n)))
    z = (l - pred) / base['sd']
    return {'z': round(float(z), 2), 'lambda1': round(l, 3), 'tokens': n,
            'expected': round(pred, 3),
            'verdict': 'well-formed' if z < 1.0 else 'unusual' if z < 2.0 else 'broken'}


def evaluate(seed=7):
    """Held-out operating characteristics. Nothing here is fitted on these sentences.

    NEGATIVE CLASS is shuffles of the held-out sentences themselves, plus the constructed
    agrammatical set. Shuffling is the right primary negative because it holds vocabulary,
    length and register fixed and destroys only the structure — so the detector cannot win
    by noticing that broken text is shorter or uses different words.
    """
    from icm_confound import AGRAMMATICAL
    from icm_parse import shuffled

    base, train, test = fit(seed=seed)
    good = [r[2] for r in test]
    broken = [shuffled(s, 900 + i) for i, s in enumerate(good)]

    zs = lambda xs: [score(x, base)['z'] for x in xs if score(x, base)['z'] is not None]
    zg, zb, za = zs(good), zs(broken), zs(AGRAMMATICAL)

    import numpy as np
    print(f'\n  held out: {len(zg)} well-formed, {len(zb)} shuffled, {len(za)} agrammatical\n')
    print(f'  {"class":<24} {"mean z":>7} {"sd":>6}')
    for name, z in (('well-formed (held out)', zg), ('shuffled', zb), ('agrammatical', za)):
        print(f'  {name:<24} {np.mean(z):>7.2f} {np.std(z):>6.2f}')

    # AUC by rank, no sklearn dependency
    def auc(pos, neg):
        allv = [(v, 1) for v in pos] + [(v, 0) for v in neg]
        allv.sort()
        ranks = {}
        i = 0
        while i < len(allv):
            j = i
            while j + 1 < len(allv) and allv[j + 1][0] == allv[i][0]:
                j += 1
            r = (i + j) / 2 + 1
            for k in range(i, j + 1):
                ranks[k] = r
            i = j + 1
        rp = sum(ranks[k] for k, (_, lab) in enumerate(allv) if lab == 1)
        n1, n0 = len(pos), len(neg)
        return (rp - n1 * (n1 + 1) / 2) / (n1 * n0)

    print(f'\n  AUC vs held-out well-formed')
    print(f'    shuffled       {auc(zb, zg):.3f}')
    print(f'    agrammatical   {auc(za, zg):.3f}')

    print(f'\n  operating points (threshold on z)')
    print(f'  {"z >":>5} {"false alarm":>12} {"caught: shuffled":>17} {"agrammatical":>13}')
    for thr in (0.5, 1.0, 1.5, 2.0):
        fpr = np.mean([v > thr for v in zg])
        t1 = np.mean([v > thr for v in zb])
        t2 = np.mean([v > thr for v in za])
        print(f'  {thr:>5.1f} {fpr:>11.1%} {t1:>17.1%} {t2:>13.1%}')
    return base


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('text', nargs='?')
    ap.add_argument('--fit', action='store_true')
    ap.add_argument('--eval', action='store_true')
    a = ap.parse_args()
    if a.fit:
        b, _, _ = fit()
        print(f"\n  fitted {b['form']}  R²={b['r2']:.3f}  sd={b['sd']:.4f}  "
              f"train {b['n_train']} / test {b['n_test']}")
    elif a.eval:
        evaluate()
    elif a.text:
        print(json.dumps(score(a.text), indent=2))
    else:
        ap.print_help()
