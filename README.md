# HarfHizlisi

Turkish word game: guess words from 3 to 9 letters across 7 rounds, plus a bonus round with no letter limit.

## Rules

- **8 questions total**: lengths 3, 4, 5, 6, 7, 8, 9, then a bonus round (any length)
- After each question starts, **one hidden letter is revealed every 7 seconds**
- Each remaining hidden letter is worth **10 points** when you answer correctly
- Answer early to maximize your score
- Guesses are **case-insensitive** (Turkish `i` / `ı` supported)

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Open [http://localhost:8000](http://localhost:8000)

Alternative (uvicorn with auto-reload):

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Deploy to Render

1. Push the repo to GitHub (or GitLab).
2. On [Render](https://dashboard.render.com): **New** → **Blueprint** → connect the repo (uses `render.yaml`),  
   **or** **New** → **Web Service** → connect the repo and set:
   - **Runtime**: Python
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `gunicorn wsgi:application --bind 0.0.0.0:$PORT` (or `gunicorn app:app --bind 0.0.0.0:$PORT`)
   - **Environment**: `PYTHON_VERSION` = `3.12.8` (avoid 3.14 until deps support it)
3. Deploy. Your app will be at `https://harf-hizlisi.onrender.com` (or the name you choose).

**Notes**

- Render sets `$PORT` automatically; do not hardcode a port in production.
- The free tier spins down after inactivity; the first request may take ~30s.
- Uploaded questions are saved to `data/questions.json` on the instance disk, which is **ephemeral** on Render — uploads are lost on redeploy unless you add persistent storage or an external store later.

## Deploy to PythonAnywhere

1. Upload or `git clone` the project to e.g. `/home/YOUR_USERNAME/HarfHizlisi`
2. Open a **Bash console** and install dependencies:

```bash
cd ~/HarfHizlisi
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Create a **Web** app (manual configuration, **Flask**).
4. Edit the WSGI file (e.g. `/var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py`):

```python
import sys

path = "/home/YOUR_USERNAME/HarfHizlisi"
if path not in sys.path:
    sys.path.insert(0, path)

from wsgi import application
```

5. In the Web tab set:
   - **Source code**: `/home/YOUR_USERNAME/HarfHizlisi`
   - **Working directory**: `/home/YOUR_USERNAME/HarfHizlisi`
   - **Virtualenv**: `/home/YOUR_USERNAME/HarfHizlisi/.venv`
6. Reload the web app.

Static files (`static/`) and the logo are served by Flask automatically.

## Soru bankası (JSON yükleme)

Örnek format: `examples/questions.example.json`

| Endpoint | Açıklama |
|----------|----------|
| `GET /api/questions/example` | Örnek JSON şablonu |
| `GET /api/questions` | Mevcut soru bankasını indir |
| `POST /api/questions/upload` | JSON ile yükle (`replace` veya `merge`) |
| `POST /api/questions/reset` | Gömülü varsayılan bankaya dön |

```bash
curl -X POST http://localhost:8000/api/questions/upload \
  -H "Content-Type: application/json" \
  -d @examples/questions.example.json
```

Yüklenen sorular `data/questions.json` dosyasına kaydedilir.

## Stack

- **Backend**: Python + Flask
- **Frontend**: HTML, CSS, vanilla JavaScript
