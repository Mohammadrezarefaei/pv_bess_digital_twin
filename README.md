# ☀️ Co-located PV-BESS Asset Digital Twin

An industrial-grade simulation and Mixed-Integer Linear Programming (MILP) optimization platform designed for co-located photovoltaic solar generation and Battery Energy Storage Systems (BESS) in European day-ahead electricity markets.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pvbessdigitaltwin-7ysrulwe6w6bkcftvfdxrp.streamlit.app/)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Overview

As renewable penetration increases across European grids, co-locating battery storage with solar PV assets provides substantial synergy. However, optimizing day-ahead dispatch schedules under volatile price spikes and varying weather profiles requires advanced mathematical modeling.

**PV-BESS Digital Twin** simulates and optimizes asset operations by solving real-time dispatch decisions, balancing solar generation, battery charging and discharging cycles, and wholesale market export strategies to maximize total daily revenue.

---

## 🚀 Key Features

* **Advanced MILP Optimization:** Solves complex mixed-integer linear programming models using PuLP to determine optimal hourly charging, discharging, and grid injection schedules.
* **Interactive Streamlit Dashboard:** Allows energy analysts and operators to dynamically adjust PV capacity, battery power ratings, energy capacity, and initial state of charge in real time.
* **Operational Analytics:** Generates clear visual profiles of solar generation, net grid export, and battery state of charge alongside detailed hourly dispatch tables.
* **Robust Automated Testing:** Includes unit tests powered by Pytest to verify database persistence and core simulation logic.

---

## 📊 Live Dashboard Preview

Access the live application deployed on Streamlit Cloud:  
👉 **[PV-BESS Digital Twin Live App](https://pvbessdigitaltwin-7ysrulwe6w6bkcftvfdxrp.streamlit.app/)**

---

## 🏗️ Repository Structure

```text
pv_bess_digital_twin/
├── database/
│   └── database_logger.py     # SQLite database persistence module
├── notebooks/
│   └── pv_bess_milp_optimization.ipynb # Jupyter notebook for mathematical modeling
├── tests/
│   ├── __init__.py
│   └── test_digital_twin.py   # Pytest unit tests for simulation logic
├── app.py                     # Interactive Streamlit dashboard UI
├── requirements.txt           # Project Python dependencies
└── README.md                  # Project documentation
