# SachAI

SachAI is a multilingual fake-news detector built with **React**, **FastAPI**, **Qdrant**, and **Gemini**.
It focuses on the kind of misinformation that spreads fast on WhatsApp, reels, and forwarded articles.

## What it does

- Paste suspicious text or a WhatsApp forward
- Upload an image for image-first verification flow.
- Search Qdrant for semantically similar misinformation patterns.
- Show a **Misinformation Family Tree** when a known fake keeps returning in new forms.
- Generate a simple, common-man explanation in **English / Hindi / Tamil / Hinglish**.
- Trigger an optional **live search fallback** when the vector match is weak.
- Display a visual **credibility score** and **fake risk meter**.

## Tech stack

### Frontend
- React + TypeScript + Vite
- Neo-Pop Brutalism UI
- Framer Motion ready

### Backend
- FastAPI
- Sentence Transformers using `intfloat/multilingual-e5-large`
- Qdrant vector database
- Gemini summarization layer using `google-genai`

## Project structure

```text
sachAI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── utils/
│   ├── scripts/
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   ├── package.json
│   └── .env.example
├── docs/
│   ├── architecture.md
│   ├── presentation-flow.md
│   ├── mentor-case-study.md
│   └── demo-script.md
├── docker-compose.yml
└── README.md
```

## 1) Start Qdrant

```bash
docker compose up -d
```

Qdrant runs at:
- REST: `http://localhost:6333`
- gRPC: `localhost:6334`

## 2) Backend setup

```bash
cd backend
python -m venv .venv
```

### Windows
```bash
.venv\Scripts\activate
```

### macOS / Linux
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Copy env:

```bash
copy .env.example .env
```

On macOS/Linux:

```bash
cp .env.example .env
```
### Required environment variables

```env
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=sach_claims
GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=gemini-2.5-flash
GOOGLE_SEARCH_API_KEY=optional_for_live_search
GOOGLE_SEARCH_ENGINE_ID=optional_for_live_search
BACKEND_CORS_ORIGINS=http://localhost:5173
```

Seed demo data:

```bash
python -m scripts.seed_data
```

Run backend:

```bash
uvicorn app.main:app --reload --port 8000
```

Backend API base:
`http://localhost:8000/api/v1`

## 3) Frontend setup

```bash
cd frontend
npm install
```

Copy env:

```bash
copy .env.example .env
```

or

```bash
cp .env.example .env
```

Run frontend:

```bash
npm run dev
```

Frontend opens at:
`http://localhost:5173`

## API endpoints

### Verify text
```http
POST /api/v1/verify
Content-Type: application/json
```

Body:

```json
{
  "text": "Free recharge link sab users ko free data de raha hai, abhi click karo aur OTP dalo.",
  "mode": "text",
  "explain_tone": "simple"
}
```

### Verify image
```http
POST /api/v1/verify-image
Content-Type: multipart/form-data
```

### Health
```http
GET /api/v1/health
```

## Demo flow

1. Paste a Hinglish scam forward.
2. Backend embeds it with multilingual E5.
3. Qdrant retrieves similar misinformation patterns.
4. If top score is high, family tree is shown.
5. Gemini writes a simple explanation.
6. UI shows credibility score + fake risk bar.

## Example demo input

```text
Free recharge link sab users ko free data de raha hai. Abhi click karo aur OTP dalo. Sab telecom users ke liye hai.
```

Expected demo story:
- Qdrant score comes high.
- Matched with 2021 scam cluster.
- Family tree shows 2021, 2022, 2023, 2024 variants.
- Response explains: this is likely phishing, do not forward, do not click, verify through the official telecom app.

## Production ideas

- Add OCR for images and keyframes for videos.
- Add fact-check ingestion pipelines from trusted publishers.
- Add admin ingestion dashboard.
- Add domain credibility intelligence.
- Add user report history and moderation workflow.

## Notes

- Image flow in this starter repo is intentionally lightweight and ready for Gemini Vision enhancement.
- Live search fallback is optional and activates only when Qdrant confidence is weak.
- The included data is demo data; replace it with real curated misinformation and fact-check corpora before deployment.
