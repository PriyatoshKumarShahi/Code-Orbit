# Presentation Flow for Mentors and Judges

## 1. Hook (10-15 sec)
"Every day, people forward messages without checking if they are true. In India, many of these are in Hinglish, regional languages, or recycled media. Veritas-AI helps any user check a suspicious message in seconds."

## 2. The problem (20 sec)
- Fake news spreads faster than official clarification.
- Common users do not read long fact-check articles.
- Most tools fail on Indian code-mixed content like Hinglish.
- The same fake story keeps returning in new versions.

## 3. Our solution (20 sec)
"Veritas-AI is a multilingual fake-news detector. A user pastes a message or uploads an image. We compare it against known misinformation patterns in Qdrant, then generate a simple explanation in everyday language."

## 4. What makes us different (30 sec)
- Hinglish-aware retrieval
- Misinformation Family Tree
- live-search fallback when database confidence is weak
- common-man explanation instead of technical output
- credibility score with visual report

## 5. Tech flow (30 sec)
- React frontend for simple UX
- FastAPI backend for orchestration
- multilingual-e5-large for embeddings
- Qdrant for similarity search
- Gemini for human-friendly explanation

## 6. Demo sequence (60 sec)
1. Paste the fake free recharge Hinglish forward.
2. Click verify.
3. Show similarity score and scam label.
4. Open family tree panel.
5. Show credibility meter going low.
6. Read the friendly summary out loud.

## 7. Impact statement (15 sec)
"We are not just saying fake or real. We are helping the user understand why a message is dangerous, where it came from, and why they should stop forwarding it."

## 8. Future roadmap (15 sec)
- video verification
- trusted-news ingestion
- region-wise language expansion
- WhatsApp bot / browser extension / public API
