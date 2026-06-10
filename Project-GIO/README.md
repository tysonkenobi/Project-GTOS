# Geometric Information Observer (GIO)

## Version: v0.2.0
## Type: Experimental Latent-State Instability Probe
## Focus: Context Drift Detection & Abstention Trigger Signals in Autoregressive Systems
## WIKI (Under Construction): https://github.com/tysonkenobi/Project-GIO/wiki

---

## 🧠 Overview

The Geometric Information Observer (GIO) is a passive diagnostic framework designed to analyze latent-state dynamics in synthetic or transformer-like generative systems.

Its goal is not to evaluate factual correctness, but to measure:

> **When a model’s internal representation begins to lose stable contextual alignment during generation.**

This condition is treated as **context drift**, which may lead to:
- hallucinated continuation
- temporal inconsistency
- loss of grounding in prior context

---

## ⚙️ Core Hypothesis

Autoregressive model failures are often preceded by measurable shifts in latent state dynamics and output distribution structure.

We hypothesize that:

> A scalar instability signal derived from latent drift + output entropy can act as an early indicator of context degradation.

---

## 📊 Key Metric: Kappaₜ (Instability Signal)

Kappaₜ is a composite scalar designed to capture latent instability.

It is defined as:

- latent state drift (temporal displacement)
- output entropy (distribution uncertainty)
- logit variance (distribution dispersion)

Combined into a single signal:

> Higher Kappaₜ values indicate increased likelihood of representation instability.

---

## 🧪 System Architecture

The framework consists of three components:

### 1. Latent State Process
Simulates or observes evolving hidden states over time.

- Supports:
  - baseline low-noise dynamics
  - perturbed drift dynamics

---

### 2. Output Projection Layer
Maps latent states into logit distributions.

- Enables entropy-based analysis of output uncertainty

---

### 3. Geometric Information Observer
Computes:

- State drift energy
- Shannon entropy
- Logit variance
- Unified instability score (Kappaₜ)

---

## 🔬 Experimental Design

The system compares two regimes:

### Baseline Process
- Stable latent evolution
- Low stochastic noise

### Drift Process
- Progressive noise injection
- Increasing representational instability

---

## 📈 Observed Behavior (v0.2)

Empirical simulations show:

- Kappaₜ increases during transition phases of latent instability
- Entropy alone does not reliably capture transitional dynamics
- Peak Kappaₜ often precedes distribution collapse or reorganization

This suggests Kappaₜ may function as:

> a **phase transition indicator for latent representation stability**

### φ³ Ratio Stability (GIO v0.2 / Narrator v0.1)

The entropy collapse rate relative to 1/φ³ was measured across three random 
seeds and two noise intensity levels. The ratio remained stable despite a 67% 
increase in noise magnitude, suggesting a structural invariant in the 
measurement geometry rather than a noise-dependent artifact.

### Entropy Collapse Rate / (1/φ³) Ratio Across Seeds and Noise Levels

| Seed | Noise Mean | Collapse Rate | 1/φ³     | Ratio    |
|------|------------|---------------|----------|----------|
| 0    | 0.3        | 0.038382      | 0.236068 | 0.162587 |
| 0    | 0.5        | 0.038600      | 0.236068 | 0.163511 |
| 42   | 0.3        | 0.038829      | 0.236068 | 0.164483 |
| 42   | 0.5        | 0.038829      | 0.236068 | 0.164483 |
| 99   | 0.3        | 0.040459      | 0.236068 | 0.171387 |
| 99   | 0.5        | 0.040795      | 0.236068 | 0.172812 |

### Difference Between Noise Levels Per Seed

| Seed | Ratio noise=0.3 | Ratio noise=0.5 | Absolute Difference |
|------|-----------------|-----------------|---------------------|
| 0    | 0.162587        | 0.163511        | 0.000924            |
| 42   | 0.164483        | 0.164483        | 0.000000            |
| 99   | 0.171387        | 0.172812        | 0.001425            |

### Summary
- Noise intensity increased by 67% (0.3 → 0.5)
- Maximum ratio shift: 0.001425
- Ratio range across all tests: 0.162587 – 0.172812
- Conclusion: Ratio stable across both seed variation and noise intensity variation
- Open question: The theoretical basis for why the ratio 
  clusters near 1/(6φ³) remains under investigation. Current hypothesis is that each Dzhanibekov correction step covers exactly 6 of these units, 
connecting to the 6 fundamental functions of the unit circle.
  
---

## 🚨 Intended Application

This framework is designed for research into:

- Context drift detection in LLMs
- Uncertainty-aware generation systems
- Abstention triggering mechanisms ("I don’t know" behavior)
- Stability monitoring in autoregressive pipelines

---

## ⚠️ Important Clarification

This project does NOT attempt to:

- model physical reality
- define semantic truth
- or propose new physics laws

All physical geometry references (black holes, event horizons) are 
inspirational frameworks that motivated the mathematical approach, 
not literal physical claims.

---

## Architecture Overview

The GIO system is split into three separate modules, each with a single responsibility.

### geometric_observer_core (gio_v02.py)
The measurement layer. Contains the `GeometricInformationObserver` class which computes 
the core kappa instability metric from latent state drift, output entropy, and logit 
variance. Also contains `BaseProcess` and `DriftProcess` for synthetic testing. 
Run directly to see a live baseline vs drift comparison experiment.

### gio_narrator (gio_narrator_v010.py)
The detection and narration layer. Wraps the observer and maintains a running history 
of states, metrics, and tokens. Detects singularity events using two methods: sudden 
entropy acceleration and sustained entropy collapse. When a singularity is found, 
reconstructs a geometrically grounded explanation of where and how the breakdown occurred.

### gio_runner (gio_runner_v010.py)
The entry point. Wires the observer and narrator together, runs the experiment, and 
reports results. This is the file you run. Modify step count and process parameters here 
without touching the core modules.

### Recommended development workflow

Run each module in sequence to verify each layer independently:

```bash
python3 gio_v02.py          # Inspect raw metrics across all steps
python3 gio_narrator_v010.py  # Confirm narrator module loads cleanly  
python3 gio_runner_v010.py    # Run full singularity detection pipeline
```

The runner alone is sufficient for production use. Running all three 
sequentially provides visual feedback at each layer during development.

---

## 🔮 Future Work

Planned extensions include:

### 1. Predictive Instability Modeling — Partially Complete
- The collapse detection in the narrator is retrospective right now, not predictive. It finds where the singularity happened after the fact. So this one is started but not done. Prediction would mean flagging it before entropy hits zero.
- Use Kappaₜ(t) to predict future entropy collapse

### 2. Abstention Trigger Integration - Detection layer complete
- Threshold-based singluarity identification implemented in gio_narrator.  Response actions (halt, fallback) pending.
- Define thresholds for:
  - “uncertain response”
  - retrieval fallback
  - generation halt

### 3. Real Transformer Integration
- Apply observer to:
  - open-weight LLM logits
  - embedding trajectories
  - attention-state dynamics

---
