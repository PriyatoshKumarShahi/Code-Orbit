import { useState } from 'react'
import { verifyImage, verifyText } from '../lib/api'
import type { VerifyResponse } from '../types/api'

export function useVerify() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<VerifyResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  async function submitText(text: string) {
    setLoading(true)
    setError(null)
    try {
      const data = await verifyText(text)
      setResult(data)
    } catch (err) {
      setError('Could not verify this message right now. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  async function submitImage(file: File) {
    setLoading(true)
    setError(null)
    try {
      const data = await verifyImage(file)
      setResult(data)
    } catch (err) {
      setError('Image analysis failed. Please try another image.')
    } finally {
      setLoading(false)
    }
  }

  return { loading, result, error, submitText, submitImage }
}
