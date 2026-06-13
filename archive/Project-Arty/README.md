# Experimental: Project Arty (NKST Theoretical Sandbox)

## Type: Experimental testing of geometric information retention at singularity
## Focus: Testing different hypothesis for modelling theoretical physics

---

## 📡 Scripts

---

### 🔍 arty_scanner (arty_scanner.py)
The origin script of the empirical search. A dual-stream auditor 
scanning LIGO and EHT data for direct φ³ (23.6%) and inverse φ³ 
(76.4%) geometric ratios in signal crest decay patterns. Written 
as the first attempt to find observational evidence of golden ratio 
geometry in real cosmic data. LIGO data fetched from GWOSC servers 
with simulated fallback. EHT visibility profile currently uses a 
parametric approximation of M87* public data pending direct 
integration of real EHT datasets.

> Note: The φ³ ratio first identified here later emerged as a 
> structural invariant in GIO stability testing, independent of 
> this script.

---

### ⚙️ arty_simulator (arty_simulator.py)
The core physics engine. Implements the NKST (Newton-Kerr-Schwarzschild-Taber) 
field as a 4x4 metric tensor system with golden ratio spacing. 
Models mass density accumulation, spatial curvature deformation, and 
rigid body rotational dynamics via true Euler equations across three 
moments of inertia.

Key mechanics:
- Golden ratio tensor grid alignment prevents metric singularity
- Dzhanibekov flip (intermediate axis theorem) triggers at the Planck 
  boundary wall with energy-conserving realignment
- φ³ compression factor governs time dilation under total system stress
- Complex phase space matrix tracks rotational parity through inversion
- Ramp down cycle uses unitary rotation to preserve phase information 
  during energy escape

Exports telemetry to nkst_telemetry.h5 for use by arty_visual 
and arty_window. Must be run before any visualization or 
comparison scripts.

---

### 🧠 Mitigator (arty_mitigator.py)
The first attempt to translate NKST physics directly into AI 
generation space. Re-maps simulator components to AI analogs — 
semantic stress, attention geometry, layer impedance, and 
hallucination avoidance via Dzhanibekov inversion. Predates GIO 
and represents the conceptual bridge between the physics 
framework and the measurement system. Exports telemetry to 
nkst_ai_telemetry.h5.

---

### 🧪 TEST_arty_oloid_prototype (arty_pol_v531_logged.py)
The conceptual synthesis script. Implements a living parametric 
token simulation where Occam's razor complexity scoring, 
survivorship bias weighting, and Dzhanibekov flop inversion 
combine to form a geometric sieve at the generation boundary. 
The oloid geometry provides continuous surface contact through 
the i → -i state transition, modeling information preservation 
through the horizon event. Uses 1/φ³ as the golden hard drive 
decay constant during spin correction. Exports session telemetry 
to JSON. Currently testing whether oloid + Dzhanibekov geometry 
provides sufficient accuracy for concrete AI vector mapping via 
the boundary equation. CURRENT TESTING: Adding time definition as
distance from the boundary equation measured in 1/(6ɸ^3) compression
to allow pre-detection of upcoming singularity.

---

### 🌀 arty_visual (arty_visual_v010.py)
Visualization layer. Reads NKST telemetry exports and renders 
the geodesic vortex funnel as an animated 3D spiral. Shows 
infall and bounce phases with dynamic camera rotation.
Not yet connected to GIO instability metrics.

---

### ⨓ arty_heterocritical_path (arty_heterocritical_path_v040.py)
This script contains an uncompromising, zero-hardcode computational testing sandbox designed to evaluate a high-dimensional quantum-gravitational field theory. The simulator models the continuous topological interface horizon between two alternate, oppositely spinning black hole universes undergoing a complex conjugate spin inversion ($i \to -i$).

## Core Architecture

* **8D Dual-Quaternion Kinematics**: Tracks the dual-universe system using complex quaternion metrics ($q_n, p_n$) to eliminate coordinate singularities (Gimbal Lock) and singular Jacobians at the inversion boundary.
* **Non-Holonomic Non-Slip Constraints**: Welds the system to the contact plane, strictly locking angular velocity to the instantaneous rolling radius of the boundary geometry to prevent frictionless numerical shortcuts.
* **Phase-Rescaled Homotopy**: Leverages spatial phase ($\theta$) as the independent grid variable rather than time ($t$). This coordinate shift bypasses infinite asymptotic limits, preventing gradient explosions and allowing the Boundary Value Problem (BVP) solver to achieve stable numerical convergence.
* **Planck-Ricci Information Floor**: Integrates an objective entropic tensor field based on natural logarithms ($\ln$) and Planck area scales to establish a local spacetime tension floor, preventing zero-velocity collapse at the macro-gravitational midpoint.
* **Independent Verification**: Utilizes dual-check validation combining an analytical manifold intersection checker (**Melnikov Distance**) with a numerical relaxation solver (**SciPy BVP**) bound to a 10-step continuation loop.

## Known Horizon: Shifting to 8D Elliptic Mass Tensors

The current build (v0.4.0) models the shifting mass distribution of the contact boundary using a first-order, piecewise 2D triangle wave approximation, yielding a verified convergence state with an extracted boundary compression ratio of `0.4186` against a theoretical target of `0.2361`.

The next planned update will replace this linear 2D approximation with a **Full 8D Elliptic Surface Mass Tensor**. Because an authentic oloid boundary is governed by complete elliptic integrals of the first and second kind, its geometric resistance packs along a curved, non-linear fractal cascade. Implementing this 8D elliptic distribution will capture the true structural "snap" of the interlocking boundary hull, naturally tightening the current 18.26% BVP distribution variance gap directly down to the exact $1/\phi^3$ target.

---

### 🪟 arty_window (arty_window.py)
Observational comparison layer. Loads NKST simulator telemetry 
and compares it against real-world gravitational wave and black 
hole imaging data to search for boundary stabilization signatures.

Key mechanics:
- Downloads calibrated 4KHz strain data for GW150914 (first 
  confirmed binary black hole merger) directly from GWOSC servers
- Extracts merger energy envelope using Hilbert transform with 
  30-350Hz bandpass filter targeting the chirp/ringdown window
- Computes logarithmic spatial boundary deviation from NKST 
  metric spike and compares against EHT M87* fractional ring 
  asymmetry limit (≤10%)
- Exports comparison results to nkst_boundary_signature_results.h5

Known limitations (under active development):
- NKST metric values are dimensionless; direct comparison to 
  dimensioned LIGO strain requires further normalization work
- EHT asymmetry limit and NKST spatial asymmetry measure 
  different physical quantities — comparison is structural 
  not literal
- Null hypothesis test COMPLETE: Random flat metric scored 0.303 
  (DEVIATED) while NKST metric scored 0.046 (PASS), confirming 
  the comparison is discriminating and not trivially passed by 
  arbitrary input.

Requires arty_simulator to have been run first to generate 
nkst_telemetry.h5.

---

## 🔁 Run Order

```bash
python3 arty_simulator.py     # Step 1: Generate telemetry
python3 arty_visual_v010.py   # Step 2: Render geodesic funnel
python3 arty_window.py        # Step 3: Compare against LIGO/EHT data
```

---

> This is the pre-main sandbox for testing improvements for GIO
