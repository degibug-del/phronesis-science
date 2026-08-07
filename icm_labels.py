#!/usr/bin/env python3
"""The last untested version of the theory: keep the labels and the direction.

    python3 icm_labels.py

WHAT WAS THROWN AWAY

Every earlier construction symmetrised the dependency tree and dropped the relation types,
leaving an unweighted undirected matrix. Two things went with them:

    direction   which token is the head and which the dependent
    labels      nsubj, det, relcl, amod — what KIND of relation each edge is

This is the last form of the original claim that has not been measured.

A BRANCH RULED OUT BEFORE IT WAS BUILT, and it is worth stating as a proof rather than
discovering by experiment: a rooted dependency tree is a DAG, so its directed adjacency
matrix is NILPOTENT and every eigenvalue is exactly zero. Measured, to be sure: max
|eigenvalue| = 0.0. So "use direction, read the eigenvalues" is mathematically empty. The
singular values are not zero and are the only way direction can enter a spectral reading.

LABEL WEIGHTS ARE DERIVED, NOT CHOSEN. Picking numbers per relation type would be tuning
with extra steps. Each edge is weighted by the surprisal of its label, -log p(label),
with p estimated from the corpora in this file — so a common `det` edge contributes little
and a rare `csubj` contributes a lot, and nothing was decided by taste.

THE TWO QUESTIONS, kept apart because they have different answers and different value:

    1. Does it reach COHERENCE — can it tell meaningful prose from grammatical nonsense?

       Predicted NO, for a reason that does not need an experiment: "colorless green ideas
       sleep furiously" is syntactically perfect at every level of description, labels and
       direction included. A purely syntactic quantity cannot see semantic emptiness. If
       this prediction fails, something is wrong with the stimuli, not with the theory.

    2. Does it make the BREAKAGE DETECTOR better — a larger effect on agrammatical text
       than the plain symmetric lambda1 managed (d = 1.63)?

       Genuinely open, and the useful outcome. The detector is the thing that survived.

═══════════════════════════════════════════════════════════════════════════════════════
RESULT, 2026-08-07: labels and direction make everything WORSE. The thesis is closed.

    reading             shuffle W/T/L   meaning p      d   breakage p      d
    sym λ1 (baseline)        1 / 0 /11       0.939   0.04       0.006   1.63
    directed σ1              1 / 5 / 6       0.254  -0.60       0.033   1.20
    labelled λ1              3 / 0 / 9       0.030  -1.27       0.188   0.69
    labelled+dir σ1          4 / 0 / 8       0.012  -1.56       0.362   0.47

Nothing reaches coherence, and every refinement degrades the breakage detector: d falls
1.63 -> 1.20 -> 0.69 -> 0.47 as more of the parse is kept. The simplest reading is the best
one, which is not the direction a theory wants to go.

THE FALSE POSITIVE, AND HOW IT DIED. The two labelled rows appeared to SEE MEANING —
p = 0.030 and p = 0.012 against grammatical nonsense — which would have overturned the
prediction written above and rescued the thesis. It was an artifact of the stimuli, and the
stimuli are mine:

    amod rate -> labelled λ1                      r = -0.629   p = 0.009
    amod rate -> condition                        r = +0.807   p = 0.0002
    condition -> labelled λ1, controlling amod    r = -0.121   p = 0.65

My nonsense sentences are adjective-stacked, because piling adjectives on nouns is HOW a
sentence is made meaningless while staying grammatical — "the quiet number ate a purple
argument". `amod` is a low-surprisal label, so more of it lowers a surprisal-weighted
lambda1. The measure was reading adjective density and the condition was perfectly
confounded with it. Partial out one variable and the effect vanishes.

Worth noting what did NOT catch this: the omnibus chi-square on the label distributions
came back p = 0.155, comfortably null, because it spreads 180 edges over 28 categories. The
confound was visible only in the single cell — amod 9.8% to 29.5% — and in the partial
correlation. An omnibus test is not a check for a confound you can name.

WHAT THIS LEAVES. Every construction of the theory has now been measured: co-occurrence
over types, co-occurrence over tokens, symmetric parse, directed parse, labelled parse,
labelled and directed parse. None measures coherence. Plain symmetric lambda1 detects
syntactic breakage at d = 1.63 and that is the instrument that exists.
═══════════════════════════════════════════════════════════════════════════════════════
"""
import collections
import math

import numpy as np
from scipy import stats

from icm_confound import NORMAL, NONSENSE, AGRAMMATICAL
from icm_parse import CORPUS, nlp, shuffled

ALL_TEXT = CORPUS + NORMAL + NONSENSE + AGRAMMATICAL


def label_surprisal():
    """-log p(label), estimated from every text this file uses. Derived, not decided."""
    counts = collections.Counter()
    for t in ALL_TEXT:
        for tok in nlp()(t):
            if tok.head.i != tok.i:
                counts[tok.dep_] += 1
    total = sum(counts.values()) or 1
    return {k: -math.log(v / total) for k, v in counts.items()}, total


SURPRISAL, _N = label_surprisal()
MEAN_SURPRISAL = float(np.mean(list(SURPRISAL.values()))) if SURPRISAL else 1.0


def matrices(text):
    """Four readings of the same parse, differing only in what was kept."""
    doc = nlp()(text)
    n = len(doc)
    if n < 2:
        return None
    sym = np.zeros((n, n))          # symmetric, unweighted — the baseline that failed
    dsym = np.zeros((n, n))         # directed head -> dependent
    lsym = np.zeros((n, n))         # symmetric, label-weighted
    ldir = np.zeros((n, n))         # directed, label-weighted
    for t in doc:
        if t.head.i == t.i:
            continue
        h, d = t.head.i, t.i
        w = SURPRISAL.get(t.dep_, MEAN_SURPRISAL)
        sym[h, d] = sym[d, h] = 1.0
        dsym[h, d] = 1.0
        lsym[h, d] = lsym[d, h] = w
        ldir[h, d] = w
    return sym, dsym, lsym, ldir


def readings(text):
    m = matrices(text)
    if m is None:
        return None
    sym, dsym, lsym, ldir = m
    top_eig = lambda A: float(np.sort(np.linalg.eigvalsh(A))[::-1][0])
    top_sv = lambda A: float(np.linalg.svd(A, compute_uv=False)[0])
    return {
        'sym λ1 (baseline)': top_eig(sym),
        'directed σ1':       top_sv(dsym),
        'labelled λ1':       top_eig(lsym),
        'labelled+dir σ1':   top_sv(ldir),
    }


KEYS = list(readings(NORMAL[0]).keys())


def paired_shuffle():
    print('\n  1 · paired shuffle — does it beat a sentence made of its own words?\n')
    print(f"  {'reading':<20} {'win':>4} {'tie':>4} {'loss':>5}")
    for k in KEYS:
        w = t = l = 0
        for i, txt in enumerate(CORPUS):
            a, b = readings(txt), readings(shuffled(txt, 1000 + i))
            if not a or not b:
                continue
            d = a[k] - b[k]
            if abs(d) < 1e-9:
                t += 1
            elif d > 0:
                w += 1
            else:
                l += 1
        print(f'  {k:<20} {w:>4} {t:>4} {l:>5}')


def dissociation():
    print('\n  2 · does it see MEANING, or only BREAKAGE?\n')
    print(f"  {'reading':<20} {'nonsense p':>11} {'d':>6}   {'agram p':>9} {'d':>6}   verdict")
    for k in KEYS:
        g = {name: [readings(x)[k] for x in texts if readings(x)]
             for name, texts in (('n', NORMAL), ('s', NONSENSE), ('a', AGRAMMATICAL))}

        def eff(x, y):
            x, y = np.array(x), np.array(y)
            s = np.sqrt(((len(x) - 1) * x.var(ddof=1) + (len(y) - 1) * y.var(ddof=1))
                        / (len(x) + len(y) - 2))
            return (y.mean() - x.mean()) / s if s > 0 else 0.0

        _, ps = stats.ttest_ind(g['n'], g['s'], equal_var=False)
        _, pa = stats.ttest_ind(g['n'], g['a'], equal_var=False)
        ds, da = eff(g['n'], g['s']), eff(g['n'], g['a'])
        if ps < 0.05:
            v = 'SEES MEANING — check the stimuli'
        elif pa < 0.05:
            v = f'breakage only (d={da:.2f})'
        else:
            v = 'sees neither'
        print(f'  {k:<20} {ps:>11.3f} {ds:>6.2f}   {pa:>9.3f} {da:>6.2f}   {v}')


if __name__ == '__main__':
    print(f'\n  labels and direction — {len(SURPRISAL)} relation types over {_N} edges')
    print(f'  surprisal range: {min(SURPRISAL.values()):.2f} ({min(SURPRISAL, key=SURPRISAL.get)})'
          f' .. {max(SURPRISAL.values()):.2f} ({max(SURPRISAL, key=SURPRISAL.get)})')
    paired_shuffle()
    dissociation()
    print('\n  baseline to beat: plain symmetric λ1 gave breakage d = 1.63, meaning p = 0.94.\n')
