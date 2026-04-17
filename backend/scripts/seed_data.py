from app.db.qdrant_client import upsert_claims

SEED_RECORDS = [
    {
        "id": "claim-001",
        "title": "Free Recharge Scam Link",
        "text": "Free recharge link sab users ko 3 mahine ka recharge de raha hai. Bas is link par click karke OTP dalo.",
        "label": "scam",
        "source": "Cyber safety archive",
        "published_at": "2021-05-12",
        "url": "https://example.org/free-recharge-scam",
        "snippet": "A phishing campaign promising free recharge in exchange for OTP.",
        "family_tree": [
            {"id": "ft-2021-a", "title": "Lockdown Free Recharge Scam", "label": "scam", "year": 2021, "variation_note": "Used OTP bait", "similarity": 0.92},
            {"id": "ft-2022-a", "title": "Festival Recharge Offer Scam", "label": "scam", "year": 2022, "variation_note": "Added wallet cashback claim", "similarity": 0.88},
            {"id": "ft-2023-a", "title": "Jio Free 84 Days Fraud", "label": "scam", "year": 2023, "variation_note": "Used shortened URL", "similarity": 0.86},
            {"id": "ft-2024-a", "title": "Election Offer Recharge Scam", "label": "scam", "year": 2024, "variation_note": "Targeted WhatsApp groups", "similarity": 0.83}
        ]
    },
    {
        "id": "claim-002",
        "title": "Old Riot Video Reused as Current Event",
        "text": "Viral video claiming current city violence actually shows footage from an unrelated 2019 incident.",
        "label": "misleading",
        "source": "Fact-check desk",
        "published_at": "2024-08-03",
        "url": "https://example.org/riot-video-old",
        "snippet": "Archived media mismatch between claim date and actual video origin.",
        "family_tree": [
            {"id": "ft-2019-b", "title": "Original 2019 clip", "label": "real-context-mismatch", "year": 2019, "variation_note": "Original upload", "similarity": 0.9},
            {"id": "ft-2024-b", "title": "Reposted with fake caption", "label": "misleading", "year": 2024, "variation_note": "Caption changed to create panic", "similarity": 0.84}
        ]
    },
    {
        "id": "claim-003",
        "title": "Government Scholarship Portal Alert",
        "text": "Official scholarship portal opens on April 20. Apply only through the .gov.in website and verify announcements on the ministry portal.",
        "label": "real",
        "source": "Education ministry archive",
        "published_at": "2025-04-18",
        "url": "https://example.org/scholarship-real",
        "snippet": "Legitimate announcement from an official domain.",
        "family_tree": []
    },
    {
        "id": "claim-004",
        "title": "Tamil Free Gift Voucher Forward",
        "text": "இது ஒரு இலவச பரிசு வவுச்சர் என்று வரும் லிங்க் மோசடி. OTP அல்லது bank details கொடுக்க வேண்டாம்.",
        "label": "scam",
        "source": "Tamil cyber awareness cell",
        "published_at": "2023-11-01",
        "url": "https://example.org/tamil-voucher-scam",
        "snippet": "Tamil phishing message offering free gift vouchers.",
        "family_tree": [
            {"id": "ft-2023-c", "title": "Festival voucher phishing", "label": "scam", "year": 2023, "variation_note": "Tamil festive bait", "similarity": 0.87}
        ]
    }
]


if __name__ == "__main__":
    upsert_claims(SEED_RECORDS)
    print("Seeded Veritas-AI demo claims into Qdrant.")
