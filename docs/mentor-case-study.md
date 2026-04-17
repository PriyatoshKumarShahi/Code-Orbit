# Mentor Case Study Narrative

## Case title
**The Free Recharge Scam in Hinglish**

## User input
"Free recharge link sab users ko free data de raha hai. Abhi click karo aur OTP dalo. Aaj last date hai."

## What happens internally

### Step 1: Language detection
The system detects a Hinglish-style message.

### Step 2: Embedding
The text is converted into a multilingual semantic vector using `multilingual-e5-large`.

### Step 3: Qdrant retrieval
Qdrant finds a high similarity match with a known scam cluster.
For demo narrative, say:
- similarity score: **0.92**
- label: **scam**

### Step 4: Family tree fetch
The system loads historical variations:
- 2021 lockdown recharge scam
- 2022 festival recharge variant
- 2023 free-data clickbait variant
- 2024 election-offer scam variant

### Step 5: LLM explanation
Gemini writes a plain-language report:

> Dhyan dein! Yeh message fake recharge scam lag raha hai. Iska similar version pehle bhi viral ho chuka hai. OTP ya personal details mat dijiye. Official telecom app ya website se hi verify kariye.

## Final output to show judges
- Verdict: **Likely Fake**
- Fake risk: **89%**
- Credibility score: **11/100**
- Family tree: visible
- Similar scams found: visible
- Advice: do not click or forward

## Why judges like this case
- instantly relatable
- India-specific
- common-man value is obvious
- shows strong AI + retrieval integration
- moves beyond classification into explanation
