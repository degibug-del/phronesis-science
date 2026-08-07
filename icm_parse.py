#!/usr/bin/env python3
"""ICM over real dependency parse trees — phase 1 of the ICM plan.

    python3 icm_parse.py

WHAT THIS SETTLES

The theory (FROM_GRAMMAR_TO_COHERENCE.md 3.2) says: parse the input into a tree following
grammatical rules, turn the tree into an adjacency matrix, read the eigenvalues. Coherence
is how far the largest eigenvalue stands above the second.

That has never been tested. The TypeScript implementation in phronesis-world/lib/icm.ts
substitutes a WORD CO-OCCURRENCE graph for the parse tree, because parsing in a Worker
without a model is hard, and on 2026-08-07 it failed a contrastive test — 2 wins, 6 ties,
4 losses against its own shuffles. Two things about that failure pointed here rather than
at the equation:

  · A co-occurrence graph over word TYPES collapses "the the the the" to a single node.
  · The graph is UNDIRECTED, so reversing a sentence preserves every adjacency pair and
    produces the identical matrix. It cannot tell a sentence from its reverse — a proof,
    not a measurement, and no threshold repairs it.

A dependency parse has neither property. Every token is its own node, and the tree of a
shuffled sentence genuinely differs from the tree of the original, because the parser reads
order. So the information the measure needs is present for the first time.

THE TEST IS THE SAME ONE, deliberately: same corpus, same degradations, so the two
constructions are comparable rather than two separate stories. Content is held fixed and
structure is destroyed; nobody has to label anything.

THE PARSE IS PORTED, NOT REINVENTED. validate_real_eeg.py already built this correctly —
spaCy dependency edges, symmetric, eigvalsh, eigs[0] - eigs[1]. It was attached to the
wrong experiment (see PROVENANCE.md). This is that construction, pointed at a test that
can answer something.

═══════════════════════════════════════════════════════════════════════════════════════
WHAT IT ANSWERED, 2026-08-07. The parse tree does not rescue the theory.

The construction was the leading suspect and it is not the culprit. With real parses the
ties disappear — the measure can finally see word order — and it still cannot use it:

    original vs shuffled     win  tie  loss
    raw gap                    5    0     7        chance
    normalised gap             5    0     7        chance
    paper's full equation      5    0     7        chance, mean margin -2.06

Sweeping every reading of the tree found the signal, in the wrong direction:

    lambda1                    1    0    11        strong, INVERTED
    Laplacian spectral radius  1    0    11        strong, INVERTED
    eigen spread               1    0    11        strong, INVERTED
    mean degree                0   12     0        ties necessarily: a tree has n-1 edges

MECHANISM. A shuffled sentence parses HUBBIER — mean max degree 0.58 higher, mean lambda1
2.52 against 2.41 — because a parser that cannot find structure attaches more tokens to
one node. Tree depth is unchanged (4.50 both). So lambda1 over a dependency tree tracks
DEGREE CONCENTRATION, and word salad wins because a confused parse is a starrier tree.

WHY INVERTING IT DOES NOT SAVE IT, which is the part that settles the question. Reading
coherence as -lambda1 passes the shuffle test 11 of 12, and then ranks:

    -1.80   "drift" six times          <- most coherent
    -2.28   a plain corpus sentence
    -2.71   "the" sixteen times
    -2.83   a considered question      <- least coherent

Repetition above articulate prose: the exact pathology this was built to fix. -lambda1 is
a length-and-simplicity proxy. It wins WITHIN a pair, where length is held fixed and only
hubbiness moves, and loses ACROSS texts, where lambda1 is dominated by size.

The within-pair and across-text signals point in opposite directions. No monotone function
of lambda1 can satisfy both, so no threshold, normalisation or sign flip repairs this. The
quantity is wrong, not its calibration.

A REMAINING CONFOUND, stated because it survives the result. Shuffled text may be hubbier
because spaCy degrades gracefully to root attachment, in which case any measure built on
this is reading PARSER CONFIDENCE rather than grammatical coherence. That would be a real
signal and a useful one — it is simply not the theory's claim, and it should not be
reported as if it were.

WHAT IS LEFT UNTESTED: the tree carries labels (nsubj, det, relcl) and direction, and both
were discarded to build a symmetric unweighted matrix. Nesting depth is the theory's own
example of difficulty and it is not spectral. If there is a structural measure here it is
more likely to be in what was thrown away than in another eigenvalue of what was kept.
═══════════════════════════════════════════════════════════════════════════════════════
"""
import numpy as np
import spacy

# ── the corpus, identical to phronesis-world/scripts/icm-contrastive.ts ────────────────
CORPUS = [
    'the model reads a sentence and returns one number that describes its shape',
    'a coherence score that rises with repetition tells someone circling one thought that their writing is perfect',
    'the dominant pattern stands out when the largest eigenvalue is well separated from the second',
    'grammatical trees have significant structural symmetry because subject verb object mirrors across many sentences',
    'when eigenvalues are close together the structure is ambiguous and several patterns compete',
    'an instrument that can only ever counsel continuing is offering encouragement rather than judgment',
    'the reference is set on the first step and cannot be revised part way through the run',
    'nothing in the trace identifies the caller so a child overwrites the ground its parent had established',
    'a threshold tuned on your own recent behaviour is exactly how an instrument comes to agree with itself',
    'the agent spells its working state into a fixed grammar and a number falls out of the spelling',
    'evidence arriving after a claim is what separates a corroborated report from a confident one',
    'measurement without a fixed reference cannot distinguish slow drift from ordinary progress',
]

LAMBDA_THRESHOLD = 2.0

_nlp = None


def nlp():
    global _nlp
    if _nlp is None:
        _nlp = spacy.load('en_core_web_sm')
    return _nlp


def adjacency(text):
    """The dependency tree as a symmetric adjacency matrix, one node per TOKEN.

    Tokens, not types — a dependency tree has a node per token by definition, and that is
    the difference that stops repetition collapsing to a single node.
    """
    doc = nlp()(text)
    n = len(doc)
    A = np.zeros((n, n))
    for t in doc:
        if t.head.i != t.i:
            A[t.i, t.head.i] = 1.0
            A[t.head.i, t.i] = 1.0
    return A


def measures(text):
    """Every candidate reading of the same spectrum, so calibration and signal stay apart.

    The question phase 1 asks is whether the INFORMATION is there, which is a question
    about ordering, not about absolute values. So the raw gap is reported beside the
    paper's normalised equation: if the raw gap separates originals from shuffles and the
    equation does not, the equation is miscalibrated. If neither separates them, the parse
    tree is not carrying the signal either and the theory is in trouble.
    """
    A = adjacency(text)
    if A.shape[0] < 2:
        return {'raw_gap': 0.0, 'norm_gap': 0.0, 'paper': 0.0, 'l1': 0.0, 'l2': 0.0}
    ev = np.sort(np.linalg.eigvalsh(A))[::-1]
    l1, l2 = float(ev[0]), float(ev[1])
    raw = l1 - l2
    norm = raw / l1 if l1 > 1e-9 else 0.0
    strength = 1 / (1 + np.exp(-5 * (l1 - LAMBDA_THRESHOLD)))
    return {'raw_gap': raw, 'norm_gap': norm, 'paper': 100 * norm * strength,
            'l1': l1, 'l2': l2}


def rng(seed):
    """Mulberry32, matching the TypeScript shuffle so the degradations are the same ones."""
    s = seed & 0xFFFFFFFF

    def nxt():
        nonlocal s
        s = (s + 0x6D2B79F5) & 0xFFFFFFFF
        t = (s ^ (s >> 15)) * (1 | s) & 0xFFFFFFFF
        t = (t + ((t ^ (t >> 7)) * (61 | t) & 0xFFFFFFFF)) & 0xFFFFFFFF ^ t
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296
    return nxt


def shuffled(text, seed):
    w = text.split()
    r = rng(seed)
    for i in range(len(w) - 1, 0, -1):
        j = int(r() * (i + 1))
        w[i], w[j] = w[j], w[i]
    return ' '.join(w)


def reversed_words(text):
    return ' '.join(reversed(text.split()))


def contrast(degrade, label):
    print(f'\n  {label}')
    print(f"  {'reading':<14} {'win':>4} {'tie':>4} {'loss':>5}   mean margin")
    for key in ('raw_gap', 'norm_gap', 'paper'):
        win = tie = loss = 0
        total = 0.0
        for i, text in enumerate(CORPUS):
            a = measures(text)[key]
            b = measures(degrade(text, i))[key]
            d = a - b
            total += d
            if abs(d) < 1e-9:
                tie += 1
            elif d > 0:
                win += 1
            else:
                loss += 1
        print(f'  {key:<14} {win:>4} {tie:>4} {loss:>5}   {total / len(CORPUS):+.3f}')


if __name__ == '__main__':
    print(f'\n  ICM over dependency parse trees — {len(CORPUS)} texts, content held fixed')
    print('  Same corpus and degradations as phronesis-world/scripts/icm-contrastive.ts,')
    print('  where the co-occurrence version went 2 win / 6 tie / 4 loss on the shuffle')
    print('  and tied 12/12 on the reverse by construction.')

    contrast(lambda t, i: shuffled(t, 1000 + i), 'original vs shuffled (seeded)')
    contrast(lambda t, i: reversed_words(t), 'original vs reversed')

    print('\n  the three cases the deployed analyzer gets backwards:')
    for text, note in [
        ('the ' * 16, 'deployed 36%'),
        ('drift ' * 6, 'deployed 99% (max)'),
        ('what exactly is the thing this instrument measures, and how would I know if it were wrong',
         'deployed 21%'),
    ]:
        m = measures(text.strip())
        print(f"    paper {m['paper']:6.2f}   raw gap {m['raw_gap']:5.2f}   "
              f"λ1 {m['l1']:.3f}  λ2 {m['l2']:.3f}   {note}")
    print()
