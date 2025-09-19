# 🌍 Africa Remote Jobs Finder

A lightweight Streamlit app that searches multiple remote-friendly job boards in real-time and filters results to show roles clearly open to candidates in Africa.

## Features
- Keyword search (e.g., `Laravel`, `Flutter`, `React`, `Fullstack`)
- Scrapes/queries multiple sources: RemoteOK, WeWorkRemotely, Remotive API
- Filters to remote roles and Africa-friendly eligibility (Africa, Global, Worldwide, EMEA, etc.)
- Interactive table with title, company, brief info, detected skills, and apply link
- No persistent storage (ephemeral results)

## Quickstart

### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Run the app
```bash
python -m streamlit run app.py --server.headless true --browser.gatherUsageStats false
```

Open the URL shown in your terminal (usually http://localhost:8501).

## Deployment

### Streamlit Community Cloud
- Push this repo to GitHub
- Create a new Streamlit app, point to `app.py`
- Set Python version and dependencies from `requirements.txt`

### Hugging Face Spaces
- Create a Space of type `Streamlit`
- Upload all files
- Set `app_file: app.py`

## Notes
- This project performs polite scraping using lightweight requests. Job board HTML/structure may change; scrapers include try/except to fail gracefully.
- Eligibility detection is heuristic-based. Always double-check job pages.

## Project Structure
```
.
├── app.py                  # Streamlit UI
├── requirements.txt       # Dependencies
├── backend/
│   ├── job_models.py      # Job model, skill detection, filters
│   ├── aggregate.py       # Orchestrates scrapers with concurrency
│   └── scrapers/
│       ├── remoteok.py
│       ├── weworkremotely.py
│       └── remotive.py
└── README.md
```

## Future Improvements
- Add more sources (Wellfound/AngelList, LinkedIn with filters, YCombinator Jobs)
- Add timezone and salary filters
- Caching with TTL to reduce requests during a session
- Better NLP for eligibility detection
