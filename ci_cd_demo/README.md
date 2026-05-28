# CI/CD Demo with FastAPI

A minimal, beginner-friendly project that teaches three real-world engineering practices:

1. **Environment variables** — keeping secrets out of your code
2. **Continuous Integration (CI)** — automatically checking that code still works on every push
3. **Continuous Deployment (CD)** — automatically shipping working code to a live server

---

## Project structure

```
ci_cd_demo/
├── app.py                        # FastAPI application
├── requirements.txt              # Python dependencies
├── .env.example                  # Template for secret variables (safe to commit)
├── .gitignore                    # Files git should never track
├── README.md                     # This file
└── .github/
    └── workflows/
        └── ci.yml                # GitHub Actions CI pipeline
```

---

## Local setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ci_cd_demo.git
cd ci_cd_demo
```

### 2. Create and activate a virtual environment

A virtual environment isolates this project's dependencies from everything else on your machine.

```bash
# Create the environment (only needed once)
python -m venv venv

# Activate it — macOS / Linux
source venv/bin/activate

# Activate it — Windows
venv\Scripts\activate
```

Your terminal prompt will show `(venv)` when it is active.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create your `.env` file

```bash
cp .env.example .env
```

Open `.env` and replace the placeholder with a real value:

```
API_KEY=my-super-secret-key
```

> **Why a `.env` file?**
> Hardcoding secrets in source code is dangerous — anyone who reads the code (or the git history) can steal them. Instead, we store secrets in a `.env` file that is listed in `.gitignore` and therefore never committed. On a hosting platform like Render, you set the same variables in the dashboard instead of a file.

### 5. Run the app locally

```bash
uvicorn app:app --reload
```

The `--reload` flag restarts the server automatically when you save a file — handy during development.

Open your browser and visit:

| URL | What it does |
|-----|-------------|
| `http://127.0.0.1:8000/` | Home — confirms the app is running |
| `http://127.0.0.1:8000/health` | Health check — returns `{"status": "ok"}` |
| `http://127.0.0.1:8000/docs` | Auto-generated interactive API docs (free with FastAPI) |

---

## How CI works

Every time you push code to the `main` branch, GitHub Actions runs the pipeline defined in `.github/workflows/ci.yml`. It:

1. Spins up a fresh Ubuntu machine in the cloud (free)
2. Installs Python 3.11
3. Runs `pip install -r requirements.txt`
4. Imports the app to verify there are no errors

If any step fails, GitHub marks the push with a red ✗ and sends you an email. You fix the problem locally and push again.

**Why this matters:** Without CI, a broken dependency or typo only surfaces when a user hits an error in production. CI catches the problem seconds after you push, while the fix is fresh in your mind.

---

## How to deploy on Render (CD)

Render watches your GitHub repository. Every time CI passes on `main`, Render automatically pulls the new code and redeploys — that is Continuous Deployment.

### Steps

1. Sign up at [render.com](https://render.com) (free tier available).
2. Click **New → Web Service** and connect your GitHub repository.
3. Fill in the settings:

   | Setting | Value |
   |---------|-------|
   | **Runtime** | Python 3 |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn app:app --host 0.0.0.0 --port 10000` |

4. Under **Environment Variables**, add:

   | Key | Value |
   |-----|-------|
   | `API_KEY` | your-real-secret-key |

   > Never paste secrets into your code. The Render dashboard is the production equivalent of your local `.env` file.

5. Click **Create Web Service**. Render builds and deploys the app. Every future push to `main` triggers a new deploy automatically.

---

## CI/CD flow — the big picture

```
You write code locally
        │
        ▼
git push to main
        │
        ▼
GitHub Actions runs CI  ──── fails? ──► red ✗, email, no deploy
        │ passes
        ▼
Render detects new commit
        │
        ▼
Render builds & restarts the app
        │
        ▼
Live site updated  ✓
```

---

## Key concepts — quick reference

| Concept | Plain-English meaning |
|---------|----------------------|
| **Environment variable** | A named value stored outside your code, loaded at runtime. Keeps secrets safe. |
| **`.env` file** | A local file holding environment variables. Never committed to git. |
| **`venv`** | An isolated folder of Python packages for this project only. |
| **CI** | Automated checks that run every time you push code. |
| **CD** | Automated deployment every time CI passes. |
| **`/health` endpoint** | A URL that returns `ok` so monitoring tools know the app is alive. |
