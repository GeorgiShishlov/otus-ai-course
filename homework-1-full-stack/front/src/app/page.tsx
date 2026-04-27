'use client'

import { useState, useEffect } from 'react'

const API = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000'

export default function Home() {
  const [questions, setQuestions] = useState<string[]>([])
  const [answers, setAnswers] = useState<string[]>([])
  const [submitted, setSubmitted] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch(`${API}/questions`)
      .then((res) => res.json())
      .then((data: { id: number; text: string }[]) => {
        setQuestions(data.map((q) => q.text))
        setAnswers(Array(data.length).fill(''))
      })
      .catch(() => setError('Не удалось загрузить вопросы. Убедитесь, что бэкенд запущен.'))
  }, [])

  const handleChange = (index: number, value: string) => {
    setAnswers((prev) => {
      const updated = [...prev]
      updated[index] = value
      return updated
    })
  }

  const handleSubmit = async (e: React.SyntheticEvent) => {
    e.preventDefault()
    try {
      const res = await fetch(`${API}/answers`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(answers),
      })
      if (!res.ok) throw new Error()
      setSubmitted(true)
    } catch {
      setError('Ошибка при отправке. Попробуйте ещё раз.')
    }
  }

  if (submitted) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="bg-white rounded-2xl shadow-md p-10 text-center max-w-md w-full">
          <h2 className="text-2xl font-semibold text-green-600 mb-2">Спасибо!</h2>
          <p className="text-gray-500">Ваши ответы приняты.</p>
        </div>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-gray-50 py-12 px-4">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-8 text-center">Мини-анкета</h1>

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-xl text-sm">
            {error}
          </div>
        )}

        {questions.length === 0 && !error ? (
          <p className="text-center text-gray-400">Загрузка вопросов...</p>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-6">
            {questions.map((question, index) => (
              <div key={index} className="bg-white rounded-2xl shadow-sm p-6">
                <p className="text-gray-700 font-medium mb-3">
                  {index + 1}. {question}
                </p>
                <textarea
                  value={answers[index]}
                  onChange={(e) => handleChange(index, e.target.value)}
                  placeholder="Ваш ответ..."
                  rows={3}
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-400 resize-none"
                />
              </div>
            ))}

            <button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 rounded-xl transition-colors"
            >
              Отправить
            </button>
          </form>
        )}
      </div>
    </main>
  )
}
