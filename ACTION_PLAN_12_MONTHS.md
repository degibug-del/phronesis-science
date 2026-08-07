# 12-Month Action Plan: From Theory to Evidence

## Vision

**End State (Month 12)**: 
Real-world empirical validation published in top-tier journal, with funding secured for Phase 2, and scientific community aware of spectral grammar theory.

---

## Month 1: Preparation & Foundations

### Week 1: Documentation & Internal Review
- [ ] Read complete theory documentation (all 8 files)
- [ ] Schedule internal team meeting (if collaborators available)
- [ ] Get feedback on theory from mentors/colleagues
- [ ] Revise MANUSCRIPT.md based on feedback
- [ ] Estimate true cost/timeline (refine budgets)

**Deliverable**: Polished MANUSCRIPT.md ready for publication

### Week 2: Identify Collaborators
- [ ] List ideal collaborators (neuroscientists, linguists, statisticians)
- [ ] Reach out via email/conference to 10-15 people
- [ ] Coffee chats/calls with 3-4 most promising
- [ ] Identify who will be co-investigators
- [ ] Negotiate roles and effort levels

**Deliverable**: Team of 2-3 co-investigators committed

### Week 3: IRB Protocol
- [ ] Write IRB protocol for Experiment 1 (real EEG sentences)
- [ ] Include all safety procedures, informed consent
- [ ] Get institutional review committee to pre-screen
- [ ] Revise based on feedback
- [ ] Submit to IRB

**Deliverable**: IRB protocol submitted (waiting for decision)

### Week 4: Prepare Grant Applications
- [ ] Choose top 3 grant targets (likely: NSF BRAIN, Templeton, NIDCD)
- [ ] Write first drafts of all 3 proposals
- [ ] Get feedback from grants office
- [ ] Meet with program officers (informal calls) to gauge interest

**Deliverable**: 3 grant proposals in advanced draft stage

---

## Month 2: Pilot Studies & Grant Submission

### Week 1-2: Pilot EEG Study
- [ ] Recruit 5-10 pilot subjects (easiest: psychology undergrads)
- [ ] Collect EEG during sentence reading task (minimal stimulus set)
- [ ] Goal: Check technical setup, data quality, analysis pipeline
- [ ] NOT for statistical analysis (too small n)

**Deliverable**: Confirmed that EEG setup works, data is clean

### Week 2-3: Pilot Data Analysis
- [ ] Process pilot data (ICA, artifact removal, spectral analysis)
- [ ] Compute Δλ for sentences
- [ ] Look for ANY relationship between Δλ and frequency
- [ ] Check that correlation isn't in completely wrong direction
- [ ] Document any unexpected findings

**Deliverable**: Pilot data analysis report (internal use only)

### Week 3-4: Submit Grants
- [ ] Finalize all grant proposals (NSF, Templeton, NIDCD)
- [ ] Get university approvals and signatures
- [ ] Submit to funding agencies
- [ ] Archive copies of submitted versions

**Deliverable**: 3 grants submitted, now in review pipeline

---

## Month 3: Subject Recruitment & Task Development

### Week 1-2: Recruitment Campaign
- [ ] Post flyers (universities, community centers, online)
- [ ] Social media campaign (if budget allows)
- [ ] Recruit 40 subjects for Experiment 1
- [ ] Verify inclusion/exclusion criteria
- [ ] Schedule participants for months 4-5

**Deliverable**: 40 consented subjects, baseline data collected

### Week 2-3: Refine Task
- [ ] Finalize 240-sentence stimulus set (Exp 1)
- [ ] Verify Δλ values (recompute to be sure)
- [ ] Pilot presentation software (Psychopy, PsychToolbox, E-Prime)
- [ ] Get feedback from 3-5 colleagues on task design
- [ ] Lock stimulus set (no further changes)

**Deliverable**: Final stimulus set with verified Δλ values

### Week 4: Equipment Setup
- [ ] Install/upgrade EEG system (if needed)
- [ ] Test recording quality with dummy recordings
- [ ] Install analysis software (MNE-Python, SPM, etc.)
- [ ] Write preprocessing pipeline (document steps)
- [ ] Dry run on sample data

**Deliverable**: EEG system operational, analysis pipeline tested

---

## Month 4-5: Core Data Collection (Experiment 1)

### Ongoing: Collect EEG Sentences (40 subjects)
- Week 1: Sessions 1-6 (6 subjects)
- Week 2: Sessions 7-14 (8 subjects)
- Week 3: Sessions 15-22 (8 subjects)
- Week 4: Sessions 23-30 (8 subjects)
- Month 5 Week 1: Sessions 31-40 (10 subjects)

**Parallel**: After each subject, quality-check data (look for artifacts, re-record if needed)

**Parallel**: Analyze first 10 subjects' data to catch any problems early

**Deliverable**: 40 complete EEG datasets + behavioral ratings

---

## Month 5-6: Analysis (Experiment 1)

### Week 1-2: Preprocessing
- [ ] Run ICA on all 40 datasets
- [ ] Remove artifacts (eye movements, muscle)
- [ ] Check quality (compare to standards in literature)
- [ ] Document any removed channels or epochs
- [ ] Save cleaned data

**Deliverable**: 40 cleaned EEG datasets, preprocessing report

### Week 2-3: Feature Extraction
- [ ] Compute spectral features for each epoch (Welch analysis)
- [ ] Extract peak frequency (4-12 Hz)
- [ ] Extract spectral width (FWHM)
- [ ] Extract power (integrated 4-12 Hz)
- [ ] Create feature table (40 subjects × 240 sentences)

**Deliverable**: EEG feature database (CSV file)

### Week 3-4: Grammar Features + Correlation
- [ ] Verify Δλ for all 240 sentences
- [ ] Compute per-subject correlations: r(Δλ, f)
- [ ] Compute group correlation: r = 0.527? (replicate synthetic)
- [ ] Run mediation analysis: Δλ → f → clarity?
- [ ] Create figures (scatter, histogram, per-subject)

**Deliverable**: Analysis report with all correlations and figures

---

## Month 6-7: Manuscript Writing (Core Paper)

### Week 1: Draft Results Section
- [ ] Write results with all statistics
- [ ] Include tables and figures
- [ ] Focus on clarity, precision

**Deliverable**: Full results section (5-10 pages)

### Week 2: Draft Methods Section
- [ ] Participants, stimuli, procedure
- [ ] EEG recording and preprocessing
- [ ] Analysis pipeline
- [ ] Verification of methods reproducibility

**Deliverable**: Full methods section (5-8 pages)

### Week 3: Draft Discussion
- [ ] Summarize main findings
- [ ] Compare to synthetic predictions (did r match?)
- [ ] Discuss implications
- [ ] Acknowledge limitations
- [ ] Propose future directions

**Deliverable**: Full discussion section (6-10 pages)

### Week 4: Polish & Submit
- [ ] Write intro (summarize theory)
- [ ] Integrate all sections
- [ ] Get feedback from collaborators
- [ ] Revise based on feedback
- [ ] Submit to journal (likely: NeuroImage, Cognitive Science, or eLife)

**Deliverable**: Manuscript submitted to journal 1

---

## Month 7: Grant Decisions + Plan Experiment 2

### Week 1-2: Grant Feedback
- [ ] NSF decision (or feedback for revision)
- [ ] Templeton decision (or feedback)
- [ ] NIDCD decision (or feedback)
- [ ] If rejected: prepare resubmission plan
- [ ] If awarded: celebrate & plan Phase 2

**Deliverable**: Funding status known, next steps clear

### Week 2-4: Design Experiment 2 (Comparative Linguistics)
- [ ] Recruit 60 subjects (bilingual: English-Japanese)
- [ ] Prepare English and Japanese stimulus sets (100 each)
- [ ] Verify translations are semantically equivalent
- [ ] Verify Δλ values for both languages
- [ ] Set up EEG protocol for bilingual study

**Deliverable**: Experiment 2 stimulus sets ready, subjects recruited

---

## Month 8: Experiment 2 Data Collection

### Week 1-4: Collect EEG (60 subjects × 2 languages)

**Timeline**:
- Sessions 1-15 (15 subjects): Week 1
- Sessions 16-30 (15 subjects): Week 2
- Sessions 31-45 (15 subjects): Week 3
- Sessions 46-60 (15 subjects): Week 4

**Parallel**: Quality check, preliminary analysis

**Deliverable**: 60 complete bilingual EEG datasets

---

## Month 8-9: Analysis (Experiment 2)

### Week 1: Preprocessing
- [ ] ICA, artifact removal, quality check (same as Exp 1)

**Deliverable**: 60 cleaned datasets

### Week 2: Feature Extraction
- [ ] Spectral features for all subjects, both languages
- [ ] Feature table: 60 subjects × 2 languages × baseline frequency + β

**Deliverable**: Bilingual feature database

### Week 3-4: Comparative Analysis
- [ ] Test: Does English f > Japanese f? (baseline difference)
- [ ] Test: Does β (sensitivity) stay constant across languages?
- [ ] Per-subject bilingual effects (frequency shift when switching languages)
- [ ] Statistical comparisons (t-tests, effect sizes)

**Deliverable**: Comparative analysis report with figures

---

## Month 9-10: Second Manuscript + Theory Refinement

### Week 1-2: Write Experiment 2 Manuscript
- [ ] Results: Grammar effect universal or language-specific?
- [ ] Discussion: Implications for universality of theory
- [ ] Integrate with Experiment 1 findings
- [ ] Target journal: Language Learning & Development or Cognition

**Deliverable**: Second manuscript submitted to journal 2

### Week 2-3: Refine Theory Based on Results
- [ ] If both experiments strong: theory validated, write synthesis paper
- [ ] If one weak: refine predictions, update THEORY_EXTENSIONS.md
- [ ] Update computational models if needed
- [ ] Write brief summary of what we learned

**Deliverable**: Updated THEORY_EXTENSIONS.md

### Week 3-4: Plan Experiments 3-4 (if funding permits)
- [ ] Music study: stimulus set of 30 compositions
- [ ] Garden-path: stimulus set of 60 critical sentences
- [ ] IRB amendments for both
- [ ] Budget estimates for scaling up

**Deliverable**: Protocols and budgets for Experiments 3-4

---

## Month 10: Conference Presentations + Outreach

### Week 1: Present at Conference
- [ ] Submit abstracts to major conferences (Society for Neuroscience, Cognitive Neuroscience Society, Linguistics Society of America)
- [ ] Prepare poster or talk (Exp 1 & 2 results)
- [ ] Attend conference (1-2 days)
- [ ] Network with researchers in field

**Deliverable**: Visible presence in scientific community

### Week 2-3: Media Outreach
- [ ] Write 1-2 page summary for general audience
- [ ] Contact science journalists
- [ ] Prepare brief explanatory video (5 minutes)
- [ ] Post to social media (Twitter, Medium)

**Deliverable**: Public awareness of spectral grammar theory

### Week 4: Preprint Publication
- [ ] Upload both manuscripts to arXiv or PsyArXiv
- [ ] Gets work into public domain quickly
- [ ] Establishes priority if others pursue similar ideas
- [ ] Cites appear immediately (doesn't wait for peer review)

**Deliverable**: Preprints published

---

## Month 11: Peer Review Cycle

### Ongoing: Respond to Reviewer Feedback
- [ ] Journal 1 (core paper) likely has reviews by now
- [ ] Journal 2 (comparative study) may have reviews
- [ ] Address all reviewer comments carefully
- [ ] Run additional analyses if requested
- [ ] Resubmit with response letter

**Deliverable**: Revised manuscripts resubmitted

### Parallel: Plan Phase 2
- [ ] If grants funded: start planning Experiments 3-6
- [ ] If grants rejected: prepare resubmission or seek bridge funding
- [ ] Recruit teams if multisite study planned
- [ ] Lock down budgets and timelines

**Deliverable**: Phase 2 research plan finalized

---

## Month 12: Consolidation & Launch Phase 2

### Week 1-2: Monitor Publication Status
- [ ] Check journal decisions (acceptances, minor revisions, rejections)
- [ ] Celebrate acceptances or prepare revisions
- [ ] Expect: 1-2 papers published, 1-2 in revision, or all in revision

**Deliverable**: 1-2 publications or clear path to publication

### Week 2-3: Phase 2 Launch
- [ ] If funding: hire postdocs, recruit for Experiments 3-6
- [ ] If no funding: apply for smaller grants or philanthropic support
- [ ] Establish research lab around spectral grammar
- [ ] Build international collaborations

**Deliverable**: Research program established for next 3 years

### Week 4: Retrospective & Celebration
- [ ] Review progress (theory → data → publications)
- [ ] Document what worked, what didn't
- [ ] Write summary report for funding agencies
- [ ] Celebrate with team

**Deliverable**: 12-month retrospective report

---

## Success Metrics (Month 12)

### Tier 1 (Critical)
- [ ] Experiments 1-2 data collected and analyzed
- [ ] Correlation r(Δλ, f) > 0.35 (significant, though possibly weaker than predicted)
- [ ] At least 1 manuscript submitted to peer-reviewed journal
- [ ] Theory documented in 8+ comprehensive papers/documents

### Tier 2 (Strong)
- [ ] 1-2 peer-reviewed papers published
- [ ] Grant funding secured ($200K+)
- [ ] Team of 2-3 collaborators committed to Phase 2
- [ ] Replicated core finding in second domain or language

### Tier 3 (Excellent)
- [ ] 2-3 papers published in top journals
- [ ] $500K+ funding secured
- [ ] Media coverage (mentioned in science news)
- [ ] Pathways to clinical applications clear

### Tier 4 (Optimal)
- [ ] Multiple papers published simultaneously
- [ ] >$500K funding, Phase 2 fully funded
- [ ] International collaboration network established
- [ ] Theory integrated into textbooks/courses

---

## Budget Tracker (12 Months)

| Category | Month | Cost | Running Total |
|---|---|---|---|
| IRB & paperwork | 1 | $2K | $2K |
| Pilot study (10 subjects) | 2 | $3K | $5K |
| Grant writing (time) | 1-4 | $5K | $10K |
| EEG rental (Exp 1) | 4-5 | $15K | $25K |
| Subject comp (40 Exp1 + 60 Exp2) | 4-8 | $20K | $45K |
| EEG rental (Exp 2) | 8 | $10K | $55K |
| Analysis software/compute | ongoing | $5K | $60K |
| Travel (conferences) | 10 | $3K | $63K |
| Misc (preprints, comms) | ongoing | $2K | $65K |

**Total 12-month cost (self-funded)**: ~$65K
**If funded via grant**: Most costs covered
**If not funded**: Expensive but possible with internal university support

---

## Contingency Plans

### If IRB Approval Delayed
- **Impact**: Data collection pushed back 1-2 months
- **Response**: Use time to refine stimulus sets, recruit more carefully, prepare analysis scripts
- **Recover**: Parallel data collection (recruit more subjects, shorten timeline)

### If EEG Quality Poor
- **Impact**: Can't reliably extract frequencies
- **Response**: Switch to higher-quality lab, upgrade equipment, process more carefully
- **Recover**: Extend data collection, add more subjects (more data = more robust average)

### If Core Effect Doesn't Replicate
- **Impact**: Theory falsified or requires major revision
- **Response**: Investigate why (confounds? measurement? real null?)
- **Recover**: Pivot to alternative hypotheses, publish null result with careful analysis
- **Lesson**: Failed theories advance science too

### If Grants Are All Rejected
- **Impact**: Funding gap for Phase 2
- **Response**: Seek bridge funding (internal university, small foundations)
- **Recover**: Phase 2 delayed 6 months but continues
- **Contingency**: Focus on maximizing impact of existing data (more publications, more conferences)

### If Journal Rejects Core Paper
- **Impact**: Disappointment, publication delay
- **Response**: Address criticisms, submit to next-tier journal
- **Recover**: Likely still publishable (even top journals reject good papers)
- **Lesson**: Rejection is normal (Nature rejects 95% of submissions)

---

## Decision Trees

### At Month 7 (After Experiment 1 Results)

```
If r > 0.45 (strong support):
  ↓
  → Continue to Experiment 2 (already underway)
  → Write Nature/NeuroImage paper
  → Launch Phase 2 (experiments 3-6)
  → Pursue major grants

If r ∈ [0.30, 0.45] (moderate support):
  ↓
  → Continue to Experiment 2 (already underway)
  → Investigate confounds
  → Write NeuroImage paper (still good)
  → Pursue smaller grants for Phase 2

If r < 0.30 (weak/no support):
  ↓
  → Complete analysis (understand why null)
  → Write null result paper (still publishable)
  → Investigate alternative hypotheses
  → Pivot theory or abandon
  → Seek smaller grants for follow-up investigation
```

### At Month 11 (Publication Decisions)

```
If 2+ papers accepted:
  ↓
  → Apply for major Phase 2 funding
  → Media outreach push
  → Build research program
  → Expand team

If 1 paper accepted, others in revision:
  ↓
  → Continue revisions aggressively
  → Use first publication to strengthen subsequent submissions
  → Seek medium-sized Phase 2 grants
  → Maintain team, slow scaling

If all papers rejected initially:
  ↓
  → Address criticisms
  → Resubmit to next-tier journals
  → Don't lose momentum
  → Smaller Phase 2 grants while waiting for publications
```

---

## Final Notes

**This is aggressive but realistic**: Months 4-8 are intense (40-60 hour weeks). Months 1-3 and 9-12 are moderate (30-40 hour weeks).

**Timeline is flexible**: Can accelerate or decelerate based on:
- Funding status
- Personnel availability
- Data quality
- Early results

**Success is not just acceptance/rejection**: Success is running rigorous experiments, getting clean data, publishing truthfully (whether positive or null), and advancing human understanding.

**This will change you**: Whether theory is right or wrong, you'll understand consciousness research better than 99% of neuroscientists. That's worth the effort.

**Ready?** Month 1 starts now. Let's go.

