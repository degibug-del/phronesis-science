# Experimental Protocols: Testing the Spectral Grammar Theory

## Part 1: Critical Experiment 1 – Real EEG Sentence Comprehension

### 1.1 Research Question
Does oscillation frequency in theta-alpha band (4–12 Hz) predict sentence comprehension clarity, mediated by grammatical spectral gap (Δλ)?

### 1.2 Design Overview

**Participants**: 40 right-handed native English speakers (age 18–35, no neurological history)

**Stimuli**: 240 sentences varying systematically in:
- Syntactic complexity (Δλ ∈ [0.3, 2.8])
- Sentence length (5–25 words)
- Ambiguity (unambiguous vs. 2–3 parse interpretations)
- Lexical frequency (common vs. rare words)

**Recording**: 64-channel EEG (10–20 system), sampling 500 Hz, referenced to Cz

**Procedure**:
1. Baseline (2 min eyes open, 2 min eyes closed)
2. Silent reading: sentence on screen for 3–5 seconds (word-by-word, self-paced or fixed)
3. Comprehension check: binary question ("Did John go to the store?" yes/no)
4. Subjective clarity: 1–10 Likert scale ("How clear was that sentence?")
5. 240 trials × ~30 seconds each = 2 hours total

### 1.3 EEG Analysis Pipeline

**Preprocessing**:
- Bandpass filter: 0.5–100 Hz
- Notch filter: 60 Hz (line noise)
- Re-reference: average reference
- ICA (independent component analysis): remove eye movements, muscle artifacts
- Epochs: −500 to +3000 ms relative to sentence onset
- Baseline correction: −500 to 0 ms

**Spectral Analysis**:
- Welch's method (256-point Hann window, 50% overlap, 1.95 Hz resolution)
- For each epoch, compute power spectrum 1–30 Hz
- Extract **peak frequency** in 4–12 Hz band (max power)
- Extract **spectral width** (full width at half maximum, FWHM)
- Extract **power magnitude** (integrated power 4–12 Hz)

**Grammar Feature Extraction**:
- Parse each sentence with spaCy (dependency parser)
- Compute adjacency matrix A
- Eigenvalue decomposition: λ₁, λ₂
- Spectral gap: Δλ = λ₁ − λ₂
- Log-transform: log_delta = log(Δλ + 1)
- Sentence length: n_words
- Ambiguity class: categorical (1 = unambiguous, 2 = mildly, 3 = highly)

### 1.4 Primary Hypothesis Tests

**H1: Spectral Gap → Oscillation Frequency**
$$f_{\text{peak}} = α + β \log(\Delta\lambda + 1) + \epsilon$$

Test: Linear regression across all 9600 trials (40 subjects × 240 sentences)
- Predict: β > 0 (higher Δλ → higher frequency)
- Expected: β ≈ 2.5 Hz per log-unit (from synthetic validation)
- Success: p < 0.001, R² > 0.15

**H2: Spectral Gap → Subjective Clarity**
$$\text{Clarity} = α + β \log(\Delta\lambda + 1) + \epsilon$$

Test: Linear regression across trials
- Predict: β > 0 (higher Δλ → higher clarity)
- Expected: β ≈ 1.5 points per log-unit (on 1–10 scale)
- Success: p < 0.01, R² > 0.20

**H3: Frequency Mediates Grammar-Clarity Link**
$$\text{Clarity} \sim \log(\Delta\lambda) → f_{\text{peak}} → \text{Clarity}$$

Test: Mediation analysis (bootstrap, 10,000 iterations)
- Does effect of Δλ on clarity go through frequency?
- Predict: 60–80% of effect mediated by frequency
- Success: indirect effect CI excludes zero, p < 0.05

**H4: Learning-Dependent Frequency Sharpening**
Divide sentences into quartiles by trial order (early → late)
- Measure spectral width (FWHM) per quartile
- Predict: FWHM decreases over time (frequency becomes more peaked)
- Expected: ~15% reduction from Q1 to Q4
- Success: p < 0.05, trend is linear

### 1.5 Secondary Analyses

**Per-Subject Correlation**:
- For each subject, correlate f_peak with log_delta across 240 sentences
- Distribution of r values (expect μ ≈ 0.50, SD ≈ 0.10)
- Compare to synthetic prediction (mean r = 0.526, SD = 0.074)

**Modulation by Sentence Properties**:
| Property | Prediction |
|---|---|
| **Sentence Length** | Longer sentences (more complexity) → higher baseline frequency |
| **Ambiguity** | Ambiguous → lower frequency (lower effective Δλ) |
| **Lexical Frequency** | Rare words → lower frequency locally (processing difficulty) |
| **Syntax Typicality** | Atypical syntax → broader frequency band (less confident) |

**Temporal Dynamics** (if using word-by-word presentation):
- Frequency evolves word-by-word
- Predict: frequency rises with each word (Δλ accumulates)
- Predict: large drop at disambiguation point (garden-path resolution)
- Measure: time-frequency plot (spectrogram) showing frequency trajectory

**Individual Differences**:
- Correlate subject-level β (sensitivity) with:
  - Reading span (working memory capacity)
  - Verbal IQ
  - Years of education
  - Language experience (bilingualism)
- Predict: higher β correlates with better language ability (more precise Δλ tuning)

### 1.6 Critical Controls

**Control 1: Frequency Not Driven by Arousal**
- Measure: heart rate, respiration (physiological baseline)
- Predict: frequency effect persists after controlling for arousal
- Test: ANCOVA with arousal as covariate

**Control 2: Frequency Not Driven by Attention**
- Measure: task performance (comprehension accuracy)
- Predict: frequency effect independent of performance
- Test: include accuracy as covariate; effect should persist
- Implication: frequency reflects structure processing, not just overall attention

**Control 3: Frequency Not Driven by Individual Word Properties**
- Compute word-level features (surprisal, frequency, age-of-acquisition)
- Predict: Δλ explains more variance than word-level features
- Test: compare model R² with/without word features
- Expect: Δλ-only model R² > 0.15; word-only model R² < 0.08

**Control 4: Effect Specific to 4–12 Hz**
- Repeat analysis in delta (1–4 Hz), beta (12–30 Hz), gamma (30–100 Hz)
- Predict: no correlation in other bands
- Test: test for interaction (frequency band × Δλ)
- Expected: significant interaction (effect only in theta-alpha)

### 1.7 Expected Results & Interpretation

**Best Case (Theory Validated)**:
- r(Δλ, f) ≈ 0.50–0.55 (similar to synthetic)
- β(Δλ → clarity) ≈ 1.2–1.5 points/log-unit
- Mediation: 70–80% of grammar-clarity effect via frequency
- Per-subject r: μ ≈ 0.50, 70% of subjects r > 0.40
- **Conclusion**: Theory is correct; proceed to mechanisms & applications

**Moderate Support (Theory Partially Correct)**:
- r(Δλ, f) ≈ 0.35–0.45 (weaker than synthetic)
- Mediation: 40–60% via frequency
- Other variables (surprisal, ambiguity) also matter
- **Conclusion**: Δλ is one factor among several; refine model

**No Support (Theory Rejected)**:
- r(Δλ, f) < 0.20, p > 0.05
- No mediation effect
- **Conclusion**: oscillation frequency driven by other factors; return to drawing board

### 1.8 Timeline & Resources

**Personnel**: 2 graduate students (2 months)
**Equipment**: EEG system (available), stimulus presentation software
**Cost**: $8K (40 subjects × $200 compensation)
**Timeline**: 8 weeks total

---

## Part 2: Critical Experiment 2 – Comparative Linguistics (SVO vs. SOV)

### 2.1 Research Question
Do baseline oscillation frequencies differ systematically between SVO (English) and SOV (Japanese) languages, predicted by differences in parse tree structure?

### 2.2 Hypothesis
SOV languages have lower average Δλ (verb appears last, flattens structure) → lower baseline frequency
SVO languages have higher average Δλ (verb appears early, creates hierarchy) → higher baseline frequency

### 2.3 Participants

**English Group** (n=20): Native English speakers, no Japanese experience
**Japanese Group** (n=20): Native Japanese speakers, fluent English (for within-subject control)
**English-Japanese Bilinguals** (n=20): Bilingual from childhood (test language switching)

Total: 60 subjects

### 2.4 Design

**Stimuli**: 
- 100 sentences in each language
- Semantically equivalent pairs (same meaning, different structure)
- Constructed to vary Δλ while controlling meaning

Example pair:
- English (SVO): "The scientist discovered the fossil in the museum"
- Japanese (SOV): "Kagakusha-wa hakubutsukan-de kaseki-o hakken-shita" (literally: "scientist-TOPIC museum-in fossil-OBJ discovered")

**Analysis**:
- Compute Δλ for English parse, Japanese parse
- Measure baseline frequency (quiet resting state, 2 min)
- Measure frequency during sentence processing
- Compare frequency distributions across languages

### 2.5 Predictions

**Prediction 2A (Baseline Frequency)**:
English baseline f > Japanese baseline f
- Expected difference: 0.5–1.5 Hz
- Interpretation: habitual processing of SVO structure → higher frequency tuning

**Prediction 2B (Within-Subject Comparison)**:
Bilinguals show frequency shifts when switching languages
- English mode → higher frequency
- Japanese mode → lower frequency
- Switching effect: Δf ≈ 0.5–1.0 Hz
- Timeline: effect emerges within 5 sentences of language switch

**Prediction 2C (Structure-Predicted Frequency)**:
Log-linear relationship holds within each language
$$f = α_{\text{lang}} + β \log(\Delta\lambda + 1)$$
- β should be similar across languages (~2.5)
- α should differ: α_English > α_Japanese
- Interpretation: universal sensitivity to Δλ, language-specific baseline

### 2.6 Critical Controls

- Phonological properties (pitch accent, syllable structure) shouldn't affect frequency
- Control by analyzing nonsense sentences (preserve syntax, eliminate meaning)
- Expected: frequency effect persists even for meaningless sentences

### 2.7 Expected Outcome

**If Supported**: 
- Major evidence for universal principle
- Shows structure, not meaning, drives frequency
- Predicts similar effects in all language pairs (VSO, OSV, etc.)

**If Not Supported**:
- Either SVO/SOV distinction doesn't matter (theory refined)
- Or baseline frequency driven by other language properties (phonology, morphology)

---

## Part 3: Music Study – Phrase Structure & Clarity

### 3.1 Research Question
Does musical phrase structure (harmonic hierarchy, cadences) exhibit spectral gap that predicts listener oscillations and subjective clarity?

### 3.2 Stimuli

**Compositions** (n=30):
- Tonal classical pieces (Bach, Mozart, Beethoven) varying in harmonic complexity
- Each piece analyzed for phrase-level harmonic structure
- Spectral gap computed for harmonic tree (I-IV-V-I structure as hierarchy)

**Clarity Predictions**:
- Clear cadences (V→I): high Δλ, predicted high f, predicted high clarity
- Deceptive cadences (V→VI): low Δλ, predicted low f, predicted low clarity
- Atonal music: Δλ ≈ 0, predicted f ≈ baseline (5 Hz), predicted low clarity

### 3.3 Design

**Participants** (n=40):
- Half musicians (5+ years formal training)
- Half non-musicians (minimal music background)

**Procedure**:
1. Listen to 30 ~30-second musical excerpts
2. Rate clarity (1–10 scale)
3. Rate engagement/interest (1–10 scale)
4. Rate emotional impact (valence, arousal; 2D scale)
5. EEG recording throughout

### 3.4 Analysis

**Harmonic Spectral Gap**:
- Parse harmonic progression as tree
- Nodes: chords (I, IV, V, VI, etc.)
- Edges: harmonic function (dominant → tonic, etc.)
- Compute Δλ of harmonic tree
- Prediction: Δλ correlates with phrase clarity

**Oscillation Frequency**:
- Extract peak frequency 4–12 Hz during each excerpt
- Predict: f increases with harmonic Δλ
- Expected: r ≈ 0.45–0.55 (similar to language)

**Musician vs. Non-Musician**:
- Predict: musicians show higher β (more sensitive to harmonic structure)
- Predict: musicians show tighter frequency tuning (lower spectral width)
- Interpretation: training enhances Δλ detection

### 3.5 Expected Findings

**Success Criteria**:
- r(harmonic_Δλ, f) > 0.40
- Clarity ratings correlated with f (r > 0.35)
- Musician-nonmusician difference in β > 0.5 Hz/log-unit
- Deceptive cadences show lower f than authentic cadences (p < 0.05)

---

## Part 4: Garden-Path Sentences – Dynamic Reanalysis

### 4.1 Research Question
When sentence structure is initially misinterpreted then corrected (garden-path effect), does oscillation frequency reflect the reanalysis?

### 4.2 Examples

- "The horse raced past the barn fell" (garden-path verb)
- "While the band played the saxophone played." (coordination ambiguity)
- "The complex houses married and single soldiers" (NP attachment)

### 4.3 Design

**Stimuli**: 60 garden-path sentences, 60 controls (unambiguous, same length)

**Procedure** (using word-by-word presentation or RSVP):
1. Each word presented for 300 ms
2. Blank for 200 ms between words
3. EEG recorded continuously

**Key Timepoints**:
- Word 1–3: initial parse (unambiguous, both GP and control)
- Word 4–6: divergence point
  - Control: continues straightforwardly
  - GP: creates contradiction, forces reanalysis
- Word 7+: clarification

### 4.4 Predictions

**Prediction 4A (Initial Parse)**:
- Early words (1–3): f(GP) ≈ f(control) (no difference yet)
- Δλ is same for both interpretations initially

**Prediction 4B (Divergence Point)**:
- GP sentences: frequency drops (lower Δλ as ambiguity revealed)
- Control sentences: frequency stable
- Magnitude: Δf ≈ 1–2 Hz drop
- Timing: effect emerges ~300 ms after critical word (processing time)

**Prediction 4C (Reanalysis Point)**:
- After clarification word: GP frequency recovers
- Final f(GP) ≈ final f(control) (both resolved to same parse)
- But temporal profile differs (recovery indicates reanalysis)

**Prediction 4D (Effort Metric)**:
- Spectral width during reanalysis: broader than baseline
- Interpretation: brain is uncertain, frequency oscillates
- Test: measure spectral width (FWHM) at divergence point
- Expect: FWHM increases by 1–2 Hz during reanalysis

### 4.5 Analysis

**Temporal Dynamics**:
- Time-frequency plot (spectrogram, 100 ms sliding window)
- Show frequency trajectory word-by-word
- Compare GP vs. control trajectories

**Event-Related Spectral Perturbation (ERSP)**:
- Baseline-correct frequency relative to pre-sentence baseline
- Identify frequency changes (increases/decreases) at critical points
- Test for interaction: condition (GP vs. control) × timepoint

**Correlation with Behavioral Measures**:
- Do subjects who show larger frequency drops also make more reading errors?
- Predict: yes (r > 0.30)

### 4.6 Expected Results

**Strong Support**:
- Clear frequency drop at divergence point in GP sentences
- Frequency recovery after clarification
- Spectral width increases during reanalysis
- **Conclusion**: Frequency dynamically reflects parse tree structure changes

---

## Part 5: Artificial Grammar Learning – Frequency Sharpening

### 5.1 Research Question
As subjects learn artificial grammar, does oscillation frequency become more tightly tuned (narrower spectral width)?

### 5.2 Rationale

If frequency reflects learned Δλ detection:
- Day 1 (no knowledge): broad frequency band (high uncertainty)
- Day 3 (learning): narrower band (increasing certainty)
- Day 5 (expert): very narrow band (automatic processing)

### 5.3 Design

**Artificial Grammar**: 
- Simple recursive grammar (e.g., sequences like aXbX where X can nest)
- Subjects learn rules through exposure + feedback

**Timeline**:
- Session 1 (Day 1): 100 trials, learning phase
- Session 2 (Day 2): 100 trials
- Session 3 (Day 3): 100 trials
- Session 4 (Day 5): 100 trials + transfer test

**Measures**:
- Behavioral: accuracy, reaction time
- Neural: oscillation frequency, spectral width, power

### 5.4 Predictions

**Prediction 5A (Behavioral Learning)**:
Accuracy increases from Day 1 (~60%) to Day 5 (~85%)
- Standard learning curve

**Prediction 5B (Frequency Sharpening)**:
Spectral width (FWHM) decreases over learning
- Day 1: ~3 Hz (broad, uncertain)
- Day 5: ~1.5 Hz (narrow, confident)
- Test: linear trend, p < 0.05

**Prediction 5C (Frequency Elevation)**:
Peak frequency increases as brain learns structure
- Interpretation: as structure becomes familiar (Δλ can be computed), brain "tunes" to higher frequency
- Day 1: f ≈ 6 Hz (low, unfamiliar)
- Day 5: f ≈ 8 Hz (higher, learned)
- Expected: +1 to +2 Hz over 5 days

**Prediction 5D (Power Amplitude)**:
Power in 4–12 Hz band increases
- Learning makes oscillations more prominent (brain commits to strategy)
- Day 1: low power (diffuse processing)
- Day 5: high power (focused, oscillatory processing)

### 5.5 Analysis

**Frequency Trajectory**:
- Plot f vs. session (Day 1 → 5)
- Fit exponential + asymptote: f(t) = f_max − (f_max − f_0) × e^(−λt)
- Estimate time constant τ = 1/λ (how fast does tuning sharpen?)
- Expected: τ ≈ 1–2 days (moderate learning rate)

**Spectral Width Trajectory**:
- Plot FWHM vs. session
- Fit inverse function: FWHM(t) = a + b × e^(−λt)
- Measure fractional reduction: (FWHM_Day1 − FWHM_Day5) / FWHM_Day1
- Expected: 40–60% reduction

**Transfer Test (Day 5)**:
- Apply learned grammar to new strings
- Predict: oscillation frequency transfers to new strings
- If f transfers, brain has learned abstract structure (not memorized specific exemplars)

### 5.6 Expected Outcome

**Strong Evidence for Learning-Dependent Tuning**:
- Frequency and spectral width track behavior
- Suggests frequency is a neural signature of structure learning
- Supports theory that brain computes and tunes to Δλ

---

## Part 6: BCI Decoding Task – Inverse Problem

### 6.1 Research Question
Can we decode what sentence someone is reading from oscillation frequency alone?

### 6.2 Design

**Closed-Set Decoding**:
- Participant reads 100 sentences silently or aloud
- Each sentence from known set of 100 options
- Real-time EEG frequency extraction
- Decoder uses inverse model to infer Δλ
- Predict sentence based on closest-match Δλ in set

### 6.3 Decoder Pipeline

**Step 1: Frequency Extraction**
- Welch analysis every 100 ms
- Extract f(t) in 4–12 Hz band
- Smooth with 500 ms moving average

**Step 2: Frequency-to-Δλ Conversion**
$$\Delta\lambda_{\text{decoded}} = \exp\left(\frac{f(t) - 5}{2.5}\right) - 1$$

**Step 3: Sentence Matching**
- Compute Δλ for each sentence in 100-sentence set
- Find closest match: arg min |Δλ_decoded − Δλ_sentence|
- Output predicted sentence

**Step 4: Probabilistic Refinement** (optional):
- Use language model: P(sentence | f) ∝ P(f | sentence) × P(sentence)
- Bayes rule: incorporate prior probability of each sentence
- Rank top-5 predictions by posterior probability

### 6.4 Predictions

**Prediction 6A (Chance Performance)**:
- Chance (random guess from 100 options): 1%
- Lower bound (if Δλ decoded with perfect fidelity): ~70%
- Expected: 40–60% (accounting for noise and ambiguity)

**Prediction 6B (Effect of Ambiguity)**:
- Unambiguous sentences: accuracy ~55%
- Ambiguous sentences (2–3 interpretations): accuracy ~35%
- Interpretation: ambiguity creates multifrequency response, harder to decode

**Prediction 6C (Effect of Training)**:
- Untrained decoder: 40% accuracy
- After training on 20 subjects: 50% accuracy
- Interpretation: individual differences in Δλ-to-frequency mapping can be learned

**Prediction 6D (Comparison to Other Features)**:
- Frequency alone: ~45% accuracy
- N400 component + frequency: ~60% accuracy
- Surprisal + frequency: ~55% accuracy
- All combined: ~70% accuracy
- Conclusion: frequency provides unique information

### 6.5 Clinical Application

**For Locked-In Syndrome Patient**:
- Patient reads text presented on screen
- System decodes which word/sentence patient is currently reading
- Output: text-to-speech synthesizer reads aloud
- Utility: allows patient to communicate by reading

**Accuracy Required**: 70%+ for practical use (allow user to correct errors)

### 6.6 Expected Outcomes

**Success**: 
- Decode above 50% accuracy
- Frequency is useful signal for language decoding
- Opens door to BCI applications

**Partial Success**:
- 40–50% accuracy
- Frequency helps, but isn't sufficient alone
- Need multimodal approach

---

## Summary: Experimental Roadmap

| Experiment | Participants | Duration | Cost | Priority | Expected r |
|---|---|---|---|---|---|
| 1. Real EEG Sentences | 40 | 2 months | $8K | Tier 1 | 0.45–0.55 |
| 2. Comparative Linguistics | 60 | 1 month | $12K | Tier 1 | 0.40–0.50 |
| 3. Music Study | 40 | 6 weeks | $8K | Tier 2 | 0.35–0.50 |
| 4. Garden-Path | 40 | 6 weeks | $8K | Tier 2 | 0.35–0.45 |
| 5. Grammar Learning | 30 | 3 weeks | $6K | Tier 2 | Qualitative |
| 6. BCI Decoding | 20 | 4 weeks | $4K | Tier 3 | ~45% acc |

**Total Investment**: ~$46K over 6 months

**If Tier 1 succeeds**: Pursue Tier 2 (domain universality)
**If Tier 1 + Tier 2 succeed**: Pursue Tier 3 (applications)

---

## Falsification Criteria

**Theory is WRONG if**:
- r(Δλ, f) < 0.25 in Experiment 1 (no correlation)
- No frequency difference between English/Japanese (Experiment 2)
- Music harmonic Δλ doesn't predict frequency (Experiment 3)
- Garden-path sentences don't show frequency changes (Experiment 4)
- Frequency doesn't sharpen with learning (Experiment 5)
- BCI accuracy < 20% (no better than noise; Experiment 6)

**Theory is CORRECT if**:
- r(Δλ, f) > 0.45 in Experiment 1
- All Tier 1 experiments show p < 0.05
- Tier 2 shows similar effects across domains
- Tier 3 (applications) works

