# Beginner-Friendly Reusable FRED Dashboard Template

This template follows the same modular structure as the example dashboard:
- `app.py` controls the dashboard page
- `config.py` controls project-specific customization
- `src/data_loader.py` fetches and aligns FRED data
- `src/analysis.py` computes summary metrics and linear regression
- `src/visuals.py` builds charts
- `narrative_blocks.py` contains optional story text helpers

## Folder structure

```bash
project/
├── app.py
├── config.py
├── narrative_blocks.py
├── requirements.txt
├── .env.example
├── README.md
├── .streamlit/
│   └── config.toml
└── src/
    ├── data_loader.py
    ├── analysis.py
    └── visuals.py
```

## What to customize first

Open `config.py` and replace every placeholder that says `FILL IN`.

Most important parts:
1. `PROJECT_TITLE`
2. `RESEARCH_QUESTION`
3. `SERIES`
4. `TARGET_VARIABLE`
5. `MODEL_FEATURES`
6. `CHART_GROUPS`
7. `START_DATE`
8. `TARGET_FREQUENCY`

## Create a virtual environment

### Mac / Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## Install packages

```bash
pip install -r requirements.txt
```

## Add your FRED API key

Copy `.env.example` to `.env` and replace the placeholder:

```env
FRED_API_KEY=your_real_key_here
```

## Run the dashboard

```bash
streamlit run app.py
```

## Common debugging tips

- If charts are blank, check `SHOW_DEBUG_TABLES` in `config.py`
- If you get a missing API key error, make sure `.env` exists
- If one series has many missing values, the start date may be too early
- If mixed-frequency series look strange, check `TARGET_FREQUENCY`
