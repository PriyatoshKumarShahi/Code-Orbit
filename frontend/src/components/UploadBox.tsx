import { ImagePlus, MessageSquareText, ShieldQuestion } from 'lucide-react'
import { useRef, useState } from 'react'

type Props = {
  loading: boolean
  onSubmitText: (text: string) => void
  onSubmitImage: (file: File) => void
}

export default function UploadBox({ loading, onSubmitText, onSubmitImage }: Props) {
  const [text, setText] = useState('Free recharge link sab users ko free data de raha hai, abhi click karo aur OTP dalo.')
  const inputRef = useRef<HTMLInputElement | null>(null)

  return (
    <section className="neo-card upload-box">
      <div className="pill-row">
        <span className="pill pink">Hindi + Tamil + English</span>
        <span className="pill yellow">Hinglish Ready</span>
        <span className="pill cyan">Qdrant Family Tree</span>
      </div>

      <div className="hero-copy">
        <h1>Paste a viral forward. Get the truth in seconds.</h1>
        <p>
          SachAI checks suspicious news against historical fake-news patterns, scam templates, and multilingual claim vectors.
        </p>
      </div>

      <label className="input-label">
        <MessageSquareText size={18} /> Paste article / WhatsApp forward
      </label>
      <textarea
        className="neo-textarea"
        rows={8}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste a suspicious claim, viral message, or article text here..."
      />

      <div className="action-row">
        <button className="neo-button primary" disabled={loading} onClick={() => onSubmitText(text)}>
          <ShieldQuestion size={18} /> {loading ? 'Checking...' : 'Verify Text'}
        </button>
        <button className="neo-button secondary" disabled={loading} onClick={() => inputRef.current?.click()}>
          <ImagePlus size={18} /> Upload Image
        </button>
        <input
          ref={inputRef}
          hidden
          type="file"
          accept="image/*"
          onChange={(e) => {
            const file = e.target.files?.[0]
            if (file) onSubmitImage(file)
          }}
        />
      </div>
      <p className="micro-copy">Tip: this demo focuses on text + image. Video verification can be added as an OCR + keyframe pipeline.</p>
    </section>
  )
}
