# HSCs Simulator

An *in silico* computational framework designed to model theoretical hematopoietic reconstitution dynamics following stem cell transplantation.

## Overview
The HSCs Simulator models post-transplant cellular dynamics across primary stem cell pools, progenitor lineages, and fully differentiated immune effector cells over a 365-day trajectory. Built on multi-branch kinetic logic, the framework evaluates cell population shifts across myeloid, erythroid, and lymphoid lineages based on user-defined initial HSC doses.

*Note: This repository represents an initial conceptual prototype. The biological parameters are currently exploratory and have not been fully derived from literature or validated against empirical clinical datasets.*

## Repository Structure & Usage
- **`gui.py` (Current Version / Primary GUI):** Features a multi-tab interactive GUI structured into **4 functional modules/tabs**, with **2 dedicated dynamic plots per tab** (covering comprehensive multi-lineage reconstitution metrics).
- **`main.py` (Legacy Script):** Contains the foundational CLI/script prototype displaying the initial 3 static diagrams.
- **`hsc_model.py` & `config.py`:** Core mathematical logic, rate constants, and configuration settings.

## Key Features
- **Exploratory Kinetic Modeling:** Simulates theoretical cell dynamics using structural growth and differentiation algorithms.
- **Advanced Graphical Interface:** Interactive 4-tab dashboard presenting 8 total visualization plots for lineage trajectories.
- **Dose-Dependent Analysis:** Evaluates bone marrow capacity thresholds and recovery trajectories.
- **Custom Reporting:** Exports structured diagnostic and kinetic summaries.

## Academic Integrity, Acknowledgment & Scope
- **AI-Assisted Development:** Generative AI tools were utilized to assist in structuring code logic, refining algorithmic architecture, and drafting project documentation.
- **Academic Disclaimer:** This software is a theoretical computational exercise designed for exploratory modeling. It is **not evidence-based, not fully literature-derived, and not clinically validated**. It must not be used for clinical diagnostics or medical decision-making.

## Future Roadmap
- Rigorous literature mining to replace exploratory values with literature-derived physiological parameters.
- Empirical parameter calibration and validation against clinical patient datasets.
- Integration of stochastic modeling to account for biological variability.

## License
Distributed under the MIT License.
