# 🚌 VeloCity: Urban Transit Management System

![Python Platform](https://img.shields.io/badge/Python-3.x-blue.svg)
![CustomTkinter Framework](https://img.shields.io/badge/GUI-CustomTkinter-darkgreen.svg)
![SQLite3 Database](https://img.shields.io/badge/Database-SQLite3-lightgrey.svg)
![ReportLab Engine](https://img.shields.io/badge/PDF-ReportLab-red.svg)

A professional, feature-rich Bus Reservation desktop application engineered with a robust Model-View-Controller (MVC) architecture. VeloCity combines a high-performance SQLite3 relational database layer with a beautiful, dynamic CustomTkinter dark-mode UI. It effectively maintains data persistence while providing distinct, secure experiences through Role-Based Access Control (RBAC).

## ✨ Feature Highlights

### 🛡️ Secure SHA-256 Password Hashing
Security is treated as a priority at every layer. All passwords passed through the active application layer are natively encoded utilizing strict `hashlib.sha256()` hashing algorithms before reaching data persistence. Passwords are never stored or retrieved as plain text.

### 💺 Asymmetric 2+3 Aircraft-Style Seating
Say goodbye to basic, rudimentary grids. The Customer dashboard leverages complex matrix algorithms to output a highly realistic `2+3` seating configuration. It reserves a completely un-clickable central aisle column, surrounded by dynamically updating Red/Green interactive status blocks.

### 🎫 High-Fidelity PDF Ticket Engine
Creating a booking leverages the ReportLab framework to generate professional, multi-format (PDF, JPG, TXT) tickets instantly. Crucially, executing a cancellation invokes an automated VOID synchronization process, guaranteeing strict system accountability and audit trails directly on your local storage.

### 🔄 Admin "U-Turn" Navigation Workflow
Empowers Administrators with seamless vertical navigation. Admins can instantly transition from high-level management interfaces down into the exact Customer seating grid, process real-time bookings on behalf of passengers, and execute a swift "U-Turn" to snap instantly back to their centralized Admin View—without ever interrupting their session.

## 🏗️ Project Architecture & Modular Breakdown

- **`main.py`**: The centralized Application Controller. Manages the primary CTk window, initializes the SQLite engine, and handles all high-level frame routing.
- **`ui_frames.py`**: The 'View' layer. Contains dedicated classes for the Login, Registration, Admin, and Customer interfaces using a stack-based layout.
- **`database.py`**: The 'Model' layer. Manages the relational SQL schema, including table initialization, complex JOIN queries for revenue reporting, and data persistence.
- **`utils.py`**: The 'Logic' layer. A utility toolkit housing the SHA-256 encryption algorithms, timestamp formatting, and the PDF generation triggers.

## 🎨 UI/UX Polishing Integrations

### 👁️ Dynamic Password Visibility Toggles
We prioritize frictionless user experiences. State-tracked visibility toggles elegantly transition between 'Slashed Eye' and 'Clear Eye' icons, allowing real-time masking and unmasking of character entries during sensitive authentication phases without data disruption.

### 🧹 Registration Buffer Clearing
Engineered to prevent overlapping authentication bugs, VeloCity actively monitors screen state transitions. Upon a successful registration or when navigating away, the underlying memory buffers aggressively clear out all sensitive `Entry` widget arrays, ensuring subsequent logins are always initiated cleanly without stale data persistence.

## 🚀 Setup Instructions

### 1. Environment Initialization
Ensure your Python environment is ready. We strongly recommend setting up a virtual environment:

```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

### 2. Dependency Installation
Install the required architectural dependencies and UI modules:

```bash
pip install customtkinter reportlab pillow
```

### 3. Launch Application
Boot the overarching application controller:

```bash
python main.py
```

### Initial Administrator Credentials
The SQLite3 engine naturally pre-seeds a root administrator profile on the first launch:
- **Username**: `admin`
- **Password**: `password123`

## 📄 License

This project and its unified architecture are licensed under the **Apache 2.0 License**.
