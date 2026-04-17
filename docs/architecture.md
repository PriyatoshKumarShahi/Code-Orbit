# SachAI Architecture

## High-level flow

```text
User Input (Text / Image)
        |
        v
React Frontend
        |
        v
FastAPI Backend
  |        |         |
  |        |         +--> Gemini LLM summary layer
  |        |
  |        +------------> Live Search Fallback (optional)
  |
  +---------------------> Embedding Service (multilingual-e5-large)
                           |
                           v
                        Qdrant
                           |
                           v
                 Similar matches + family tree
```

## Components

### 1. Frontend
The React frontend collects:
- pasted article text
- WhatsApp forward text
- uploaded image

It displays:
- verdict
- explanation
- fake risk meter
- credibility score
- similar matches
- misinformation family tree

### 2. FastAPI backend
Main responsibilities:
- normalize multilingual input
- create semantic embedding
- query Qdrant
- compute credibility score
- trigger live search fallback when needed
- call Gemini for human-friendly summary

### 3. Embedding layer
Model:
- `intfloat/multilingual-e5-large`

Why this model:
- good multilingual retrieval
- strong for code-mixed content like Hinglish
- works well for semantic similarity and retrieval pipelines

### 4. Qdrant
Stores claim vectors with payload metadata.

Each point stores:
- text
- title
- label (`real`, `fake`, `scam`, `misleading`)
- source
- published date
- snippet
- family tree metadata

### 5. Gemini layer
Gemini does not decide the truth alone.
It explains the evidence in a friendly tone.

That means:
- retrieval decides evidence
- Gemini explains the result simply

This makes the system more trustworthy in demos.

## Credibility scoring logic

Suggested formula in this starter:
- retrieval signal from Qdrant
- top-label anchor (fake/real/scam/misleading)
- heuristic scam signals
- lexical overlap with top match

Displayed as:
- fake probability
- credibility score out of 100
- color band (`Low`, `Medium`, `High`)

## Family Tree concept

When a suspicious story matches a known fake cluster, we show earlier variations.

Example:
- 2021: lockdown recharge scam
- 2022: festival voucher scam
- 2023: free 84-day data scam
- 2024: election gift offer scam

This is a powerful demo feature because it shows that misinformation mutates instead of disappearing.

## Optional live search fallback

If Qdrant score is low:
- use Google search API or another search provider
- fetch recent public coverage
- attach a short live-search note in the report

## Suggested production improvements

- OCR pipeline for images
- ASR + OCR for videos
- claim extraction before retrieval
- hybrid search with dense + sparse vectors
- reranker before final verdict
- curated trusted-source knowledge base
