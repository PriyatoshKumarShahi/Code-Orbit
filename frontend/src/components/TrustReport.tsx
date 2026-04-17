import { AlertTriangle, SearchCheck, Sparkles } from 'lucide-react'
import type { VerifyResponse } from '../types/api'
import CredibilityMeter from './CredibilityMeter'
import FamilyTree from './FamilyTree'
import SectionTitle from './SectionTitle'

export default function TrustReport({ result }: { result: VerifyResponse | null }) {
  if (!result) {
    return (
      <section className="neo-card placeholder-card">
        <h2>No report yet</h2>
        <p>Your trust report will appear here with verdict, credibility score, evidence, and misinformation family tree.</p>
      </section>
    )
  }

  return (
    <section className="neo-card trust-report">
      <div className="report-header">
        <div>
          <span className={`status-tag ${result.visual_meter.verdict_color}`}>{result.verdict}</span>
          <h2>{result.short_verdict}</h2>
          <p>{result.explanation}</p>
        </div>
        <CredibilityMeter score={result.credibility_score} fakeProbability={result.fake_probability} />
      </div>

      <div className="report-grid">
        <div className="report-panel soft-yellow">
          <SectionTitle icon={<AlertTriangle size={18} />} title="Why we flagged it" subtitle="Common-man language, not robotic jargon" />
          <ul className="bullet-list">
            <li>Top Qdrant similarity score: <strong>{result.evidence.qdrant_score}</strong></li>
            <li>Language mode detected: <strong>{result.language_mode}</strong></li>
            <li>Confidence in verdict: <strong>{Math.round(result.confidence * 100)}%</strong></li>
            {result.evidence.live_search_used && <li>Live web verification was triggered for extra checking.</li>}
          </ul>
        </div>

        <div className="report-panel soft-cyan">
          <SectionTitle icon={<SearchCheck size={18} />} title="Closest matches" subtitle="Earlier claims that look very similar" />
          <div className="match-list">
            {result.similar_matches.slice(0, 3).map((match) => (
              <article key={match.id} className="match-card">
                <h4>{match.title}</h4>
                <p>{match.snippet}</p>
                <div className="meta-row">
                  <span className="chip">{match.label}</span>
                  <span className="chip">score {match.score}</span>
                </div>
              </article>
            ))}
          </div>
        </div>
      </div>

      <div className="report-panel soft-pink">
        <SectionTitle icon={<Sparkles size={18} />} title="Misinformation Family Tree" subtitle="Show judges how the same story mutates over time" />
        <FamilyTree nodes={result.family_tree} />
      </div>

      {result.evidence.live_search_summary && (
        <div className="report-panel soft-white">
          <SectionTitle icon={<SearchCheck size={18} />} title="Live Search Fallback" subtitle="Used when vector match is weak" />
          <p>{result.evidence.live_search_summary}</p>
        </div>
      )}
    </section>
  )
}
