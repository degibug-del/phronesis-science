# Failure Analysis: What Could Go Wrong & Alternative Theories

## Part 1: Graceful Failure Modes

### Scenario 1: Weak Correlation (r = 0.25-0.40)

**What It Means**: Δλ predicts f, but weakly

**Most Likely Cause**: 
- Δλ is one factor among many
- Other variables matter more (surprisal, frequency, ambiguity)
- Noise is higher than modeled

**Evidence**:
- Some subjects show strong effect (r > 0.50), others weak (r < 0.20)
- High per-subject variability (SD > 0.12)
- Effect present but washes out in group averages

**How to Respond**:
1. **Don't abandon theory**: Weak effect ≠ false effect
2. **Identify moderators**: Which subjects show strong vs. weak effects?
3. **Add covariates**: Working memory capacity, language ability, attention
4. **Multi-model**: Build predictive model with Δλ + other variables
5. **Publish as partial support**: Still publishable in good venues
6. **Pivot to mechanism**: Why is effect weaker? Study β-sensitivity in individuals

**Revised Theory**:
$$f = \alpha + \beta_1 \log(\Delta\lambda + 1) + \beta_2 \cdot \text{surprisal} + \beta_3 \cdot \text{frequency} + \epsilon$$

Some journals that would publish weak effect: Cognitive Science, NeuroImage, Brain and Language

**Timeline to Publication**: 4-6 months
**Impact**: Still interesting, opens new questions

---

### Scenario 2: No Effect in Real Data (r < 0.15)

**What It Means**: Synthetic validation worked, but real EEG doesn't follow theory

**Most Likely Causes**:
1. **Experimental design flaw**: Sentences not time-locked to EEG properly
2. **Measurement noise**: Real EEG much noisier than synthetic
3. **Individual variability**: Some brains follow rule, others don't
4. **Wrong frequency band**: Effect in different band (delta, beta, gamma)
5. **Wrong metric**: Not peak frequency, but power, entropy, or phase

**Evidence**:
- Correlation near zero across subjects
- No systematic relationship
- Effect doesn't replicate across subjects
- Per-subject r values have no pattern (random)

**How to Respond**:

**Step 1: Debug the Method**
- [ ] Check preprocessing (is data contaminated?)
- [ ] Verify time-locking (are epochs aligned correctly?)
- [ ] Test spectral analysis (try different methods: Welch vs. wavelet vs. FFT)
- [ ] Check signal quality (compare to literature benchmarks)

**Step 2: Check for Hidden Effects**
- [ ] Analyze different frequency bands (slow down, speed up search)
- [ ] Look at oscillation power, not just frequency
- [ ] Check phase locking between regions (maybe IFG-ATL coupling, not absolute f)
- [ ] Look at time-frequency dynamics (frequency may change word-by-word)

**Step 3: Interrogate the Data**
- [ ] Subset by language ability: Do better language users show effect?
- [ ] Subset by task performance: Do correct comprehensions show effect?
- [ ] Subset by sentence type: Does effect appear for some sentence types?
- [ ] Subset by subject attention: Do attentive subjects show effect?

**Step 4: Revise Theory**
- Maybe frequency is epiphenomenal (not causal)
- Maybe other brain areas matter more than IFG/ATL
- Maybe timing matters (early, mid, late sentence processing)
- Maybe individual differences (neural efficiency) obscure group effect

**If Nothing Works**: Theory is likely wrong. But:
- Publish negative result (important for field)
- Propose alternative: What does predict f? (surprisal? entropy? prediction error?)
- Don't just discard work; learn from failure

**Venues for null results**: PLOS ONE, eLife (accepts negative results), Cortex

**Timeline to Publication**: 3-4 months (once you understand why null)

**Impact**: Closes off this hypothesis, guides future work

---

### Scenario 3: Effect Is There But Weak in Some Domains

**What It Means**: Works for language, doesn't work for music/vision

**Most Likely Cause**:
- Language brain is different from music/vision brain
- Spectral grammar principle is language-specific, not universal
- Different domains use different neural codes

**Evidence**:
- Real EEG sentences: r = 0.50 (strong, language)
- Music harmonic: r = 0.15 (weak, music)
- Visual scenes: r = 0.10 (very weak, vision)

**How to Respond**:

**Option 1: Accept Limitation**
- Theory is specifically a theory of language, not all hierarchy
- Still valuable (language is most interesting case)
- Modify claims: "Spectral grammar explains language processing"
- Remove universal claims from papers

**Option 2: Investigate Why Domains Differ**
- Music: Maybe frequency band is wrong? Try 1-4 Hz (slower)
- Vision: Maybe spatial hierarchy different than temporal hierarchy?
- Motor: Maybe proprioceptive feedback modulates effect?
- Ask: What's different about music vs. language processing?

**Option 3: Refine Theory for Each Domain**
$$f_{\text{language}} = 5 + 2.5 \log(\Delta\lambda)$$
$$f_{\text{music}} = 2 + 1.5 \log(\Delta\lambda)$$
$$f_{\text{vision}} = 3 + 2.0 \log(\Delta\lambda)$$

Different baselines and sensitivities by domain (β varies)

**Impact**: Theory is more refined but less universal. Still publishable.

---

### Scenario 4: Confounding Variables Explain Everything

**What It Means**: Correlation exists but isn't causal; something else drives both Δλ and f

**Candidate Confounds**:
1. **Sentence length**: Longer sentences → higher Δλ, also higher f (arousal)
2. **Word frequency**: Rare words → lower Δλ, also higher f (effort)
3. **Surprisal**: Unexpected words → lower Δλ, also lower f (prediction)
4. **Semantic complexity**: Complex meaning → any Δλ, also higher f

**Evidence**:
- Correlation disappears when you control for confound
- Confound alone predicts f better than Δλ
- β reduces from 2.5 to 0.3 after controlling

**How to Respond**:

**Step 1: Quantify Confound**
- Measure confound for each sentence
- Compute partial correlation: r(Δλ, f | confound)
- How much of effect remains?

**Step 2: Design Controls**
- Create matched sentence sets (high Δλ low-surprisal, low Δλ high-surprisal)
- Within-subject controls (same sentence, different context)
- Manipulate confound independently

**Step 3: Mediation Analysis**
$$\text{Effect of } \Delta\lambda \text{ on } f \text{ via } \text{[confound]?}$$

If confound mediates 100% of effect:
- Δλ doesn't directly cause f
- Δλ predicts f only through confound
- Theory needs revision

**If confound mediates 40% of effect**:
- Δλ has direct effect (60%)
- Also indirect effect via confound (40%)
- Theory still valid, but more complex

**Impact**: Doesn't kill theory, makes it more nuanced

---

## Part 2: Hard Falsifications (Theory is Actually Wrong)

### Hard Falsification 1: Frequency Doesn't Correlate with Clarity

**What It Means**: f predicts Δλ, but doesn't predict subjective clarity

**Test**:
- Have subjects rate clarity (1-10) for each sentence
- Measure r(f, clarity)
- Prediction: r > 0.40
- If r < 0.15: theory is falsified

**Why It Would Matter**:
- Theory claims f ∝ clarity ∝ Δλ
- If f ∝ Δλ but f ∝/ clarity, then link is broken
- Frequency might be epiphenomenal

**Implication**: 
- Brain oscillations don't encode subjective experience
- Need different theory of consciousness
- Frequency is side-effect of something else

---

### Hard Falsification 2: Δλ Not Present in Brain

**What It Means**: Brain doesn't compute eigenvalues at all

**Tests**:
1. **Direct**: Record from IFG, look for eigenvalue-like signals (neural synchrony patterns)
2. **Lesion**: Damage math centers, see if grammar understanding fails
3. **Modeling**: Train neural network on language; does it learn eigenvector representations?

**Evidence for Falsification**:
- Brain doesn't show eigenvalue signatures
- Loss of math ability doesn't affect grammar
- Neural networks don't naturally learn eigenvalues

**Implication**:
- Brain uses different computation (maybe surprisal, entropy, something else)
- Theory is metaphor, not description
- Need different neural mechanism

---

### Hard Falsification 3: Frequency Before Parse Tree

**What It Means**: Brain sets frequency first, then parses according to frequency

**Evidence**:
- Frequency established before comprehension (baseline, not driven by structure)
- Different sentences (different Δλ) don't change frequency
- Instead, frequency determines how brain parses

**Implication**:
- Causality is backwards: f → Δλ, not Δλ → f
- Theory is not about grammar driving frequency
- Theory is about frequency constraints on how we parse

**This would be interesting but wouldn't kill theory**:
- Just changes interpretation (frequency is prior, not consequence)
- Still explains behavior
- Mechanism is different but principle is similar

---

## Part 3: Alternative Explanations

### Alternative 1: Surprisal Theory

**Claim**: EEG frequency correlates with word surprisal (prediction error), not grammar structure

**Mechanism**:
- High surprisal words → unexpected, hard to predict → lower frequency (difficulty)
- Low surprisal words → predictable → higher frequency (ease)
- Inverse of spectral gap theory

**Test**:
- Compute surprisal for each word (using language model)
- Compare r(surprisal, f) vs. r(Δλ, f)
- If r(surprisal, f) > r(Δλ, f), surprisal wins

**Prediction**:
- This theory would show: r(surprisal, f) ≈ 0.40-0.50
- Spectral theory would show: r(Δλ, f) ≈ 0.40-0.50
- Need to distinguish experimentally

**How to Test**:
- Create sentence pairs: high Δλ low-surprisal vs. low Δλ high-surprisal
- If Δλ matter: first pair → high f, second pair → low f
- If surprisal matter: first pair → low f, second pair → high f
- Prediction diverges

**Outcome**:
- Both matter (plausible): Frequency = f(Δλ, surprisal)
- Only surprisal matters: Theory is wrong
- Only Δλ matters: Spectral theory is right

---

### Alternative 2: Arousal/Attention

**Claim**: EEG frequency correlates with arousal level, not grammar

**Mechanism**:
- Engaging sentences → high arousal → higher frequency
- Boring sentences → low arousal → lower frequency
- Spectral gap happens to correlate with engagement (confound)

**Test**:
- Measure arousal (heart rate, pupil dilation, self-report)
- Correlate arousal with frequency
- Control for arousal in Δλ-f correlation

**Prediction**:
- Arousal accounts for 30-50% of frequency variance
- After controlling for arousal, r(Δλ, f) drops to <0.20
- Theory is confounded by arousal

**How to Test**:
- Design sentences low-Δλ high-engagement and high-Δλ low-engagement
- If arousal: high-engagement → high f regardless of Δλ
- If Δλ: high-Δλ → high f regardless of engagement

---

### Alternative 3: Lexical Frequency Effect

**Claim**: Frequency correlates with word frequency (common vs. rare words), not grammar

**Mechanism**:
- Common words → fast lexical access → higher cortical frequency
- Rare words → slow access, need more processing → lower frequency
- Δλ correlates with word frequency (complex structures use rare words)

**Test**:
- Compute average word frequency for each sentence
- Compare r(word-frequency, f) vs. r(Δλ, f)

**How to Distinguish**:
- Sentences with high-Δλ all common words
- Sentences with low-Δλ all rare words
- If word frequency matters: mixed results
- If Δλ matters: clear effect

---

### Alternative 4: Phase Resetting (Not Frequency)

**Claim**: Brain doesn't oscillate at specific frequency; instead it resets phase at parse boundaries

**Mechanism**:
- Parse tree creates "reset points" (clause boundaries, verb positions)
- Brain resets phase at these points (alpha reset)
- Looks like frequency change but is actually phase reset
- Spectral gap determines how many reset points

**Test**:
- Compute instantaneous frequency from Hilbert transform
- Compute phase reset / discontinuity
- Does Δλ predict phase resets better than it predicts frequency?

**Implication**:
- Not oscillation but phase resets
- Still correlates with Δλ (your theory could be right)
- But mechanism is different (discrete resets vs. continuous resonance)

---

### Alternative 5: Alpha Reactivity (Not Prediction)

**Claim**: Grammar-related alpha suppression (desynchronization), not frequency shift

**Mechanism**:
- Grammar processing → attention → alpha suppression (power ↓, not f shift)
- Complex grammar (high Δλ) → more attention → more suppression
- Looks like frequency change because background alpha disappears

**Test**:
- Measure alpha power (8-12 Hz band power), not just peak frequency
- Distinguish: f shift vs. power change
- Correlate Δλ with power amplitude, not frequency

**How to Distinguish**:
- If theory is right: frequency shifts, power constant
- If alpha reactivity: frequency stable, power changes dramatically

---

## Part 4: Recovery Plan If Theory Is Wrong

### If Core Effect Isn't Real (r < 0.25)

**Step 1: Accept Failure Gracefully**
- Not a waste; negative results are valuable
- Publish the null finding
- Help future researchers avoid same path

**Step 2: Post-Hoc Analysis**
- What DOES predict EEG frequency?
- Surprisal? Entropy? Prediction error? Something novel?
- Comprehensive variable analysis

**Step 3: Propose New Theory**
- Use your experimental data to develop new hypothesis
- Maybe grammatical frequency-following responses (FFRs)?
- Maybe spectral analysis at different timescales?

**Step 4: Reposition Work**
- "We tested spectral grammar theory and found no support"
- "However, we discovered that [X] predicts brain oscillations"
- "These findings suggest a new direction for consciousness research"

**Step 5: Move Forward**
- Write book: "The Theories That Failed" (valuable retrospective)
- Consult for others testing spectral grammar
- Don't let failure define you

### If Theory Is Partially Right

**Step 1: Characterize Limitations**
- Language-specific or universal? (Test music)
- Real or artifact? (Design controls)
- Causal or correlational? (Use lesion studies)

**Step 2: Refine Theory**
- Modify predictions based on what works
- Expand to what it explains well
- Narrow claims about what it doesn't explain

**Step 3: Develop Extensions**
- If language-specific: Why? What's special about language brain?
- If partially causal: What causes the rest? 
- If artifact: What's the real phenomenon underneath?

**Step 4: Build on Success**
- What percentage of literature does refined theory explain?
- Can it predict individual differences?
- Does it matter for clinical applications?

---

## Part 5: Epistemic Strategy

### Principle 1: Assume You're Probably Wrong

**Rationale**: Most theories are wrong; base rates suggest yours is too

**Implication**: 
- Design experiments to kill theory, not confirm it
- Look for disconfirming evidence first
- Celebrate failed predictions as learning

### Principle 2: Multiple Specification

**Approach**:
- Pre-register primary hypothesis
- Pre-register 3-4 alternative hypotheses
- Commit to testing all fairly
- No p-hacking or cherry-picking

**Expected Outcome**:
- Primary hypothesis: 25% chance
- One alternative: 50% chance
- Null finding: 25% chance
- Some combo is true

### Principle 3: Fail Fast, Learn Quick

**Timeline**:
- Quick pilot (1 month) to check feasibility
- If promising: full study (3 months)
- If promising: replication (3 months)
- If consistent: then theorize and publish

**Cost**: $10K pilots prevent $100K+ wasted grants

### Principle 4: Seek Disconfirming Evidence

**Active Falsification**:
- What would kill your theory?
- Design experiment to test that
- Hope to find problems early
- Fix or abandon before big investment

**Contrast with**:
- Confirmatory approach (look only for support)
- Results in wasted time and p-hacking

---

## Conclusion: Hope for the Best, Prepare for the Worst

**Best Case Scenario**: 
- Theory is right; strong effects in human brain
- Multiple domains show universality
- Opens new field of spectral linguistics
- Applications to AI and consciousness
- Career-making research

**Realistic Case**:
- Theory is partially right
- Some effects, some confounds, some individual differences
- Publishable, interesting, incremental progress
- Solid contribution to field

**Worst Case**:
- Theory is wrong; effects don't replicate
- But rigorous negative result advances science
- You become expert in what doesn't work
- Foundation for better theories

**Probability Distribution**:
- P(strong support): 20%
- P(partial support): 50%
- P(weak support): 20%
- P(no support): 10%

**Expected Value**: Even at 10% chance of being right, the impact (consciousness research) makes it worth investigating.

**Next Step**: Run the experiments and find out what the brain actually does.

