export type FamilyTreeNode = {
  id: string
  title: string
  label: string
  year?: number | null
  variation_note?: string | null
  similarity?: number | null
}

export type SimilarMatch = {
  id: string
  title: string
  label: string
  score: number
  source?: string | null
  published_at?: string | null
  url?: string | null
  snippet?: string | null
}

export type VerifyResponse = {
  verdict: 'Likely Fake' | 'Suspicious' | 'Likely Real' | 'Needs More Evidence'
  short_verdict: string
  explanation: string
  language_mode: string
  credibility_score: number
  fake_probability: number
  confidence: number
  visual_meter: {
    fake_probability: number
    credibility_score: number
    verdict_color: 'red' | 'yellow' | 'green'
    trust_band: 'Low' | 'Medium' | 'High'
  }
  family_tree: FamilyTreeNode[]
  similar_matches: SimilarMatch[]
  evidence: {
    qdrant_score: number
    matched_label_distribution: Record<string, number>
    matched_claim_ids: string[]
    live_search_used: boolean
    live_search_summary?: string | null
  }
  normalized_input: string
  extracted_text_from_image?: string | null
}
