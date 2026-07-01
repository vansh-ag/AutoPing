# 🚀 AutoPing

AutoPing is an AI-powered website submission automation tool built with **FastAPI** and **Playwright**.

It automates submitting websites to multiple online ping/indexing services through a unified API, eliminating repetitive manual work.

---

## ✨ Features

- FastAPI REST API
- Playwright browser automation
- Modular handler architecture
- Multiple website submission support
- Automatic screenshots
- Submission status tracking
- Configurable selectors
- Extensible architecture for new websites
- CAPTCHA detection (Work in Progress)

---

# 🏗️ Architecture

```
                FastAPI
                   │
                   ▼
        Submission Orchestrator
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
   Handler 1   Handler 2   Handler N
        │          │          │
        ▼          ▼          ▼
      Playwright Browser Manager
                   │
                   ▼
             Chromium Browser
```

Each website has its own isolated handler, making it easy to maintain and extend.

---

# 📂 Project Structure

```
backend/

├── app/
│
├── api/
│   └── submission.py
│
├── handlers/
│   ├── base_handler.py
│   ├── pingmyurls.py
│   ├── pingomatic.py
│   ├── bulklink.py
│   ├── wmtools.py
│   ├── prepostseo.py
│   ├── pingler.py
│   ├── smallseotools.py
│   └── duplichecker.py
│
├── playwright/
│   └── browser_manager.py
│
├── orchestrator/
│   └── submission_orchestrator.py
│
├── schemas/
│
├── config/
│   ├── selectors.py
│   └── sites.py
│
├── captcha/
│   ├── detector.py
│   ├── manager.py
│   ├── hcaptcha_solver.py
│   └── turnstile_solver.py
│
├── verification/
│
└── screenshots/
```

---

# 🌐 Supported Websites

| Website | Status |
|----------|--------|
| PingMyUrls | ✅ Working |
| Ping-O-Matic | ✅ Working |
| BulkLink | ✅ Working |
| WMTools | ✅ Working |
| PrePostSEO | ✅ Working |
| Pingler | ✅ Working |
| SmallSEOTools | 🟡 CAPTCHA Detection |
| DupliChecker | 🟡 Cloudflare Turnstile |

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/vansh-ag/AutoPing.git
```

Go to project

```bash
cd AutoPing/backend
```

Create virtual environment

```bash
uv venv
```

Install dependencies

```bash
uv sync
```

Install Playwright browser

```bash
uv run playwright install chromium
```

Run the project

```bash
uv run uvicorn app.main:app --reload
```

Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

# 📥 Example Request

```json
{
  "url": "https://example.com",
  "title": "Example Website",
  "rss_url": "https://example.com/rss.xml",
  "category": "Technology",
  "email": "admin@example.com"
}
```

---

# 🛠 Tech Stack

- Python
- FastAPI
- Playwright
- Pydantic
- Uvicorn
- UV Package Manager

---

# 📸 Screenshots

Screenshots of submissions are automatically saved in:

```
screenshots/
```

These are useful for debugging failed submissions.

---

# 🧩 Design Principles

- Modular architecture
- One handler per website
- Shared browser lifecycle
- Centralized selectors
- Extensible configuration
- Reusable verification utilities

---

# 🚧 Roadmap

## Phase 1 ✅

- FastAPI API
- Browser Manager
- Playwright Integration
- Base Handler
- Submission Orchestrator

## Phase 2 ✅

- PingMyUrls
- Ping-O-Matic
- BulkLink
- WMTools
- PrePostSEO
- Pingler

## Phase 3 🚧

- hCaptcha Detection
- Cloudflare Turnstile Detection
- CAPTCHA Screenshot Extraction
- AI-assisted CAPTCHA Solver

## Phase 4

- Background Job Queue
- Parallel Website Submission
- Retry Mechanism
- Browser Context Pooling
- Dashboard
- Docker Deployment

---

# 💡 Future Improvements

- Parallel execution
- Redis queue
- WebSocket progress updates
- Background workers
- Docker support
- AI CAPTCHA solving
- Multi-browser support
- Automatic retries
- Result dashboard

---

# 👨‍💻 Author

**Vansh Agarwal**

GitHub: https://github.com/vansh-ag

---

# 📄 License

This project is licensed under the MIT License.