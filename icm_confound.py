#!/usr/bin/env python3
"""Does lambda1 measure grammatical coherence, or only whether spaCy could parse the text?

    python3 icm_confound.py

WHY THIS IS THE EXPERIMENT WORTH RUNNING

On 2026-08-07, sweeping every spectral reading of a dependency tree found exactly one
strong signal: lambda1 separates a sentence from its own shuffle 11 times out of 12. It
does so INVERTED — the shuffle scores higher — and the mechanism looked like hubbiness: a
parser that cannot find structure attaches more tokens to one node, and a starrier tree has
a larger lambda1.

If that is right, lambda1 is reading PARSER CONFUSION rather than coherence. That is not a
worthless outcome. A reliable detector of "this text is structurally broken" is a real
instrument, and one this project could ship honestly. It is simply not the claim the theory
makes, and the two must not be reported as the same thing.

THE DISSOCIATION. Coherence and parseability travel together in ordinary text, so ordinary
text cannot separate them. Two conditions pull them apart:

    grammatical nonsense    perfect syntax, no meaning
                            "colorless green ideas sleep furiously"
    agrammatical sense      broken syntax, obvious meaning
                            "me want food go store now"

PREDICTIONS, WRITTEN BEFORE THE RUN so the result can embarrass them:

    if lambda1 tracks PARSEABILITY
        nonsense groups with normal      (both parse cleanly)
        agrammatical groups with shuffled (both parse badly)

    if lambda1 tracks COHERENCE / meaning
        nonsense groups with shuffled     (both mean nothing)
        agrammatical groups with normal   (both mean something)

    if it tracks neither, the four conditions do not separate at all.

LENGTH IS MATCHED, and the first run is why. Unmatched stimuli — nonsense and agrammatical
at ~7 words against normal at ~12 — put the two SHORT conditions at the two lowest lambda1
and the two long ones at the top, because lambda1 grows with graph size. The design was
measuring word count. All four conditions now sit at ~12 words, which is also what makes
this comparable to the shuffle test, where length is fixed by construction.

ROOT ATTACHMENT is measured alongside as the mechanism check: the fraction of tokens whose
head is the sentence root. If confusion really does flatten the tree toward a star, this
rises exactly where lambda1 does, and the story is one story rather than two coincidences.

═══════════════════════════════════════════════════════════════════════════════════════
THE ANSWER, 2026-08-07: PARSEABILITY. lambda1 reads syntax and cannot see meaning at all.

Length-matched at ~12 words, n=8 per condition, Welch t against normal:

    condition               mean λ1   root rate     Δλ1        p    Cohen d
    normal                    2.311       0.278       —        —          —
    grammatical nonsense      2.315       0.240   +0.004    0.939       0.04
    agrammatical sense        2.505       0.312   +0.195    0.006       1.63
    shuffled normal           2.400       0.316   +0.089    0.358       0.48

Meaning is invisible: perfect syntax carrying no meaning whatsoever sits 0.004 from
ordinary prose, p = 0.94, d = 0.04. That is as flat as a null gets, and it is the half of
the prediction that had to hold for the interpretation to be clean.

Breakage is loud: text with obvious meaning and broken syntax reads as the MOST damaged of
all four conditions, above even the shuffle, with a large effect at a small n.

So the 11-of-12 shuffle result was never coherence. ICM's spectral half is a SYNTACTIC
BREAKAGE DETECTOR — it answers "is this well-formed", not "is this any good". That is a
real instrument and an honest one, and it is not what the theory claimed.

WHAT WOULD OVERTURN THIS: n is 8 per condition, one parser, one language, and the stimuli
were written by the same person who wrote the prediction. The across-group shuffle contrast
is not significant (p = 0.36) while the PAIRED shuffle test was 11 of 12 — consistent,
because pairing removes between-text variance, but worth stating rather than smoothing.
The nonsense null is the load-bearing result and it is the one most worth replicating with
stimuli somebody else wrote.
═══════════════════════════════════════════════════════════════════════════════════════
"""
import numpy as np

from icm_parse import adjacency, nlp, shuffled

NORMAL = [
    'the model reads a sentence and returns one number that describes its shape',
    'the dominant pattern stands out when the largest eigenvalue is well separated',
    'when eigenvalues are close together the structure is ambiguous',
    'the reference is set on the first step and cannot be revised later',
    'evidence arriving after a claim separates a corroborated report from a confident one',
    'a threshold tuned on your own behaviour is how an instrument comes to agree with itself',
    'the agent spells its working state into a fixed grammar every step',
    'measurement without a fixed reference cannot distinguish drift from progress',
]

# Syntactically impeccable, semantically empty. Every one parses cleanly.
NONSENSE = [
    'the quiet number ate a purple argument beneath the sleeping municipal ocean',
    'several transparent Tuesdays married the loud gravity that photographed her wooden laughter',
    'his rectangular opinion drank the eighth melody while four invisible questions waited',
    'a curious silence rented the tired velocity from every borrowed patient triangle',
    'the distant permission counted nine sleeping oceans before the green idea arrived',
    'her wooden laughter forgave the loud gravity that married a purple Tuesday',
    'four invisible questions photographed the rectangular opinion inside a curious municipal silence',
    'the patient triangle drank several transparent arguments beneath his tired velocity today',
]

# Syntactically broken, meaning obvious to any reader.
AGRAMMATICAL = [
    'me want food go store now because no have money at home',
    'yesterday he not come work because sick very and no call me',
    'the book on table is mine so give me please right now',
    'we going tomorrow morning if rain not come and car still work',
    'she run more fast than him but he stronger in the arm',
    'him and me was there before you arrive at the party last',
    'the car it broken so I walking to office every day this',
    'no can finish the work today because too many thing to do',
]


def lambda1(text):
    A = adjacency(text)
    if A.shape[0] < 2:
        return 0.0
    return float(np.sort(np.linalg.eigvalsh(A))[::-1][0])


def root_rate(text):
    """Fraction of tokens attached directly to the sentence root — how star-like the parse is."""
    doc = nlp()(text)
    if not len(doc):
        return 0.0
    roots = {t.i for t in doc if t.head.i == t.i}
    return sum(1 for t in doc if t.head.i in roots and t.i not in roots) / len(doc)


def summarise(name, texts):
    l = [lambda1(t) for t in texts]
    r = [root_rate(t) for t in texts]
    w = [len(t.split()) for t in texts]
    return name, float(np.mean(l)), float(np.std(l)), float(np.mean(r)), float(np.mean(w))


if __name__ == '__main__':
    conditions = [
        ('normal', NORMAL),
        ('grammatical nonsense', NONSENSE),
        ('agrammatical sense', AGRAMMATICAL),
        ('shuffled normal', [shuffled(t, 500 + i) for i, t in enumerate(NORMAL)]),
    ]
    print('\n  does lambda1 read coherence, or parseability?\n')
    print(f"  {'condition':<22} {'mean λ1':>8} {'sd':>6} {'root rate':>10} {'mean words':>11}")
    rows = []
    for name, texts in conditions:
        row = summarise(name, texts)
        rows.append(row)
        print(f'  {row[0]:<22} {row[1]:>8.3f} {row[2]:>6.3f} {row[3]:>10.3f} {row[4]:>11.1f}')

    norm, nons, agr, shuf = (r[1] for r in rows)
    print('\n  distances in λ1 from the two anchors:')
    for label, v in (('grammatical nonsense', nons), ('agrammatical sense', agr)):
        print(f'    {label:<22} |to normal| {abs(v - norm):.3f}   '
              f'|to shuffled| {abs(v - shuf):.3f}   -> groups with '
              f'{"NORMAL" if abs(v - norm) < abs(v - shuf) else "SHUFFLED"}')

    nons_side = 'NORMAL' if abs(nons - norm) < abs(nons - shuf) else 'SHUFFLED'
    agr_side = 'NORMAL' if abs(agr - norm) < abs(agr - shuf) else 'SHUFFLED'
    print('\n  VERDICT')
    if nons_side == 'NORMAL' and agr_side == 'SHUFFLED':
        print('    PARSEABILITY. Syntax decides it and meaning does not touch it. λ1 is a')
        print('    structural-breakage detector — a real instrument, and not the theory\'s claim.')
    elif nons_side == 'SHUFFLED' and agr_side == 'NORMAL':
        print('    MEANING. Astonishing for an unlabelled adjacency spectrum; check for a')
        print('    confound in the stimuli before believing it.')
    else:
        print('    NEITHER cleanly. The conditions do not dissociate on λ1, so the 11-of-12')
        print('    shuffle result is not explained by parseability either — and length is the')
        print('    first thing to rule out, since λ1 grows with graph size.')
    print()
