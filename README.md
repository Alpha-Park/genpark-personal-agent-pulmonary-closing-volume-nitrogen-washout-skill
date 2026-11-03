# Pulmonary Closing Volume & Nitrogen Washout (SBN2) Skill

[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Zero Dependencies](https://img.shields.io/badge/zero--dependencies-standard--lib-brightgreen.svg)](requirements.txt)
[![MCP Protocol Ready](https://img.shields.io/badge/mcp-protocol--ready-orange.svg)](mcp_server.py)
[![OpenClaw Certified](https://img.shields.io/badge/openclaw-certified-purple.svg)](SKILL.md)

Zero-dependency sovereign personal agent skill for non-invasive evaluation of Single-Breath Nitrogen Washout (SBN2) Closing Volume (CV), Closing Capacity (CC), and early peripheral small airway closure.

```mermaid
flowchart TD
    InhaleO2["100% O2 Vital Capacity Inhalation from RV"] --> ExhaleWashout["Slow Exhalation Flow Rate (0.5 L/s)"]
    ExhaleWashout --> AnthonisenPhases["Continuous N2 Concentration & Volume Tracing"]
    AnthonisenPhases --> Phase3["Phase III Alveolar Slope (%N2/L)"]
    AnthonisenPhases --> Phase4["Phase IV Inflection Point (Closing Volume CV)"]
    Phase3 & Phase4 --> SmallAirwayEngine["Small Airway Patency & Ventilation Heterogeneity Score"]
    SmallAirwayEngine --> Agent["OpenClaw / Hermes Personal Agent Interventions"]
```

## Features
- **Deterministic Math**: Pure Python standard library implementation with zero external dependencies.
- **Pulmonary Physiology Standards**: Implements validated equations for Closing Volume percentage, Closing Capacity, and age-predicted reference intervals.
- **Small Airway Disease Detection**: Highly sensitive detection of bronchiolar collapse before changes in $FEV_1$ or $FVC$.
- **Model Context Protocol (MCP)**: Native JSON-RPC tool integration for LLMs and autonomous agents.

## Quickstart

```python
from client import PulmonaryClosingVolumeClient

client = PulmonaryClosingVolumeClient()
result = client.evaluate_closing_volume(
    vital_capacity_l=4.8,
    closing_volume_l=0.62,
    residual_volume_l=1.35,
    phase3_slope_pct_n2_per_l=1.1,
    age_years=28
)
print("Closing Volume %:", result["cv_vc_pct"], "%")
print("Small Airway Score:", result["small_airway_score"])
print("Classification:", result["classification"])
```

## License
Apache-2.0
