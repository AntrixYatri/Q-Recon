# QCR AI – Quality Control Record Discrepancy Detection System

QCR AI is an advanced, automated quality-monitoring audit platform built for rural road construction projects under the **Smart India Hackathon (SIH) 2026**. The platform automates text extraction, layout normalization, record matching, and discrepancy resolution across Quality Control Registers (QCR), test datasheets, and official QM E-Forms.

---

## Project Features

* **Multi-Doc Ingestion**: Accepts images and scans of road registers (PNG, JPG, WEBP) and parses them via OCR.
* **Layout Line Reconstruction**: Uses coordinate-overlap algorithms to cluster word boundaries into reading lines.
* **Standardized Normalization**: Converts disparate measurement formats (e.g. centimeters to millimeters, ratio formatting) and maps inspections dates to check compliance.
* **Discrepancy Resolver**: Compares fields across multiple documents for same roads/projects, identifying:
  1. Numerical discrepancies (e.g. GSB layer thickness deficiencies, concrete strength logs).
  2. Missing fields and out-of-bounds metrics.
  3. Timing and date mismatches.
  4. Contractor/inspector name spelling variations.
* **Executive Dashboard**: A premium, responsive React-based admin control panel showcasing critical warning status counts and interactive comparison sheets.

---

## Architecture Overview

```text
QCR-SIH/
│
├── frontend/                  # React + Vite client (JavaScript, Vanilla CSS)
│   ├── src/
│   │   ├── components/        # Reusable dashboard widgets
│   │   ├── pages/             # App views: Home, Upload, Dashboard, Results
│   │   ├── services/          # REST Client (api.js) connecting to backend
│   │   ├── App.jsx            # State Router & Sidebar layout
│   │   └── main.jsx           # Core client mount
│   └── package.json
│
├── backend/                   # FastAPI Server (Python 3.8+)
│   ├── app/
│   │   ├── main.py            # CORS middleware and routing init
│   │   ├── api/routes/        # Endpoints: health, upload, analysis
│   │   ├── services/          # Service layer communicating with ai_engine
│   │   └── models/            # Input/Output validation (Pydantic schemas)
│   └── requirements.txt
│
├── ai_engine/                 # Independent Modular AI Pipeline
│   ├── pipeline.py            # Orchestrator running OCR & discrepancy checks
│   ├── extraction/            # OCR, pdf and bounding box geometry
│   ├── preprocessing/         # String cleaners and date/unit normalizers
│   ├── document_processing/   # QCR layout parsing and label matchers
│   ├── discrepancy_engine/    # Comparative rules checking
│   └── scoring/               # Severity & confidence calculations
│
├── data/                      # File uploads and JSON audit report cache
├── tests/                     # Unit test scripts
└── notebooks/                 # Jupyter reference prototypes
```

---

## Installation & Setup

### Prerequisites

* Node.js (v16+)
* Python (v3.8+)

---

### 1. Setting Up the AI Engine & Backend

Open a terminal at the project root and navigate to `backend/`:

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/Scripts/activate   # For Windows Power Shell
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: Includes EasyOCR, PyTorch, OpenCV (headless), FastAPI, and Uvicorn.*

3. **Run Backend Server**:
   ```bash
   python app/main.py
   ```
   The backend will launch at `http://localhost:8000`. You can inspect the interactive Swagger API docs at `http://localhost:8000/docs`.

---

### 2. Setting Up the Frontend

Open a separate terminal window and navigate to `frontend/`:

1. **Install Node Packages**:
   ```bash
   npm install
   ```

2. **Launch Dev Server**:
   ```bash
   npm run dev
   ```
   The Vite React dev client will boot at `http://localhost:5173`. Open this URL in your web browser.

---

### 3. Running Automated Tests

To verify that the backend routers, validation schemes, and response shapes compile:

```bash
python -m unittest tests/test_backend.py
```

---

## API Documentation Summary

| Protocol | Endpoint | Request Body | Response Description |
| :--- | :--- | :--- | :--- |
| **GET** | `/health` | None | Returns connectivity state and services verification status. |
| **POST** | `/upload` | Multipart File (`file`), Doc Category (`document_type`) | Saves physical records, executes EasyOCR, and returns mapped keys. |
| **POST** | `/analyze` | JSON: `{"analysis_id": "proj-101"}` | Triggers AI comparison engine rules, scoring, and returns discrepancy list. |
| **GET** | `/results/{analysis_id}` | None | Fetches saved audit JSON report for a specific project. |
