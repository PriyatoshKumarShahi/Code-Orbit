import { Newspaper, ShieldEllipsis } from 'lucide-react'
import TrustReport from '../components/TrustReport'
import UploadBox from '../components/UploadBox'
import { useVerify } from '../hooks/useVerify'

export default function App() {
  const { loading, result, error, submitText, submitImage } = useVerify()

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon"><ShieldEllipsis size={20} /></div>
          <div>
            <strong>SachAI</strong>
            <span>Multilingual Fake News Detector</span>
          </div>
        </div>
        <div className="headline-tag"><Newspaper size={16} /> Trust before forward</div>
      </header>

      <section className="layout-grid">
        <UploadBox loading={loading} onSubmitText={submitText} onSubmitImage={submitImage} />
        <TrustReport result={result} />
      </section>

      {error && <div className="error-banner">{error}</div>}
    </main>
  )
}
