<p align="center">
<img src="https://img.shields.io/badge/PHOENIX-V2.0_ACCOUNTING_SYSTEM-red?style=for-the-badge&logo=python&logoColor=white">
</p>

<h1 align="center">🔥 Phoenix Automation Engine v2.0</h1>

<p align="center">
<b>Intelligent Administrative Management System & Fiscal Data Automation</b>
<br>
<i>Optimizing accounting workflows with a scalable, modular architecture.</i>
</p>

<p align="center">
<img src="https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python">
<img src="https://img.shields.io/badge/Architecture-Modular_Package-green?style=flat-square">
<img src="https://img.shields.io/badge/Status-In_Development-yellow?style=flat-square">
<img src="https://img.shields.io/badge/Focus-Dominican_Republic_Tax_Compliance-red?style=flat-square">
</p>

---

## 🚀 Project Vision
**Phoenix** is more than just a script; it is an automation engine designed to eliminate human error in accounting data processing. Our vision is to transform manual administrative burdens into a seamless digital workflow, allowing the system to make logical decisions based on fiscal rules (NCF, ITBIS, RNC).

> "Phoenix was born from the need for efficiency, evolving from a simple tool into a robust and scalable platform."

---

## 📦 Version 2.0 Core Features
The system has been migrated to a **Professional Modular Structure**, ensuring each component is independent and easy to maintain:

* **Warehouse Module (Bodega):** Centralized management of companies and fiscal identity validation (RNC).
* **Operations Module:** Logical processing of expenses, telecommunications, and restaurant services.
* **Intelligent Validation:** A rule engine ensuring the integrity of dates, amounts, and data types.
* **Tax Management:** Pre-structured data handling for fiscal reports (Dominican 606/607 formats).

---

## 🧠 Scalable Architecture
Unlike linear systems, Phoenix utilizes a **Package-based Architecture**:

```text
Proyecto_Phoenix_v2/
│
├── main.py                 # Main orchestrator (UI & Menu)
└── modules/                # The "Brain" of the system
    ├── __init__.py         # Package initializer
    ├── bodega.py           # Entity management & storage
    ├── operaciones.py      # Fiscal transaction logic
    ├── consultas.py        # Search & filtering engine
    └── validaciones.py     # Security layer & business rules