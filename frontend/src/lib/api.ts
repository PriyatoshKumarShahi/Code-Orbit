import axios from 'axios'
import type { VerifyResponse } from '../types/api'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1',
})

export async function verifyText(text: string): Promise<VerifyResponse> {
  const { data } = await api.post<VerifyResponse>('/verify', {
    text,
    mode: 'text',
    explain_tone: 'simple',
  })
  return data
}

export async function verifyImage(file: File): Promise<VerifyResponse> {
  const formData = new FormData()
  formData.append('file', file)
  const { data } = await api.post<VerifyResponse>('/verify-image', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}
