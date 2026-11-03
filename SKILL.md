---
name: genpark-personal-agent-pulmonary-closing-volume-nitrogen-washout-skill
version: 1.0.0
description: Zero-dependency sovereign personal agent skill for calculating Single-Breath Nitrogen Washout (SBN2) Closing Volume (CV/VC %), Closing Capacity (CC/TLC %), and peripheral small airway patency.
author: AlphaPark Inc.
license: Apache-2.0
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
metadata:
  openclaw_compatible: true
  hermes_compatible: true
  zero_dependency: true
---

# Pulmonary Closing Volume & Nitrogen Washout (SBN2) Skill

A sovereign personal agent capability for assessing dependent small airway (< 2mm) patency, ventilation distribution heterogeneity, Closing Volume ($CV / VC \times 100\%$), and Closing Capacity ($CC / TLC \times 100\%$).

## Core Capabilities
- **Anthonisen Four-Phase Washout**: Identifies Phase III alveolar plateau slope ($\Delta N_2\%/\text{L}$) and Phase IV onset signifying terminal bronchiolar closure.
- **Dynamic Closing Capacity**: Formulates $CC = CV + RV$ relative to Total Lung Capacity ($TLC$) and Functional Residual Capacity ($FRC$).
- **Early Small Airway Disease Screening**: Detects peripheral airway collapse years before standard spirometric $FEV_1$ decline.
- **Breathing Pattern Optimization**: Prescribes positive end-expiratory pressure breathing exercises, indoor aerosol air purification, and diaphragmatic ventilation training.

## Fast Invocation
```python
from client import PulmonaryClosingVolumeClient

client = PulmonaryClosingVolumeClient()
res = client.evaluate_closing_volume(
    vital_capacity_l=4.8,
    closing_volume_l=0.62,
    residual_volume_l=1.35,
    phase3_slope_pct_n2_per_l=1.1,
    age_years=28
)
print("Closing Volume %:", res["cv_vc_pct"], "%")
print("Small Airway Score:", res["small_airway_score"], "/ 100")
```
