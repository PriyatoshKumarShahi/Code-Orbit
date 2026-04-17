export default function CredibilityMeter({ score, fakeProbability }: { score: number; fakeProbability: number }) {
  return (
    <div className="meter-wrap">
      <div className="meter-labels">
        <span>Fake Risk</span>
        <strong>{Math.round(fakeProbability * 100)}%</strong>
      </div>
      <div className="meter-track">
        <div className="meter-fill" style={{ width: `${Math.round(fakeProbability * 100)}%` }} />
      </div>
      <div className="cred-box">
        <span>Credibility Score</span>
        <strong>{score}/100</strong>
      </div>
    </div>
  )
}
