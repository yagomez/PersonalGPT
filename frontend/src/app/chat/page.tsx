// Chat page placeholder
"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAuthStore } from "@/lib/store"

export default function ChatPage() {
  const router = useRouter()
  const { isAuthenticated } = useAuthStore()

  useEffect(() => {
    if (!isAuthenticated) {
      router.push("/login")
    }
  }, [isAuthenticated, router])

  if (!isAuthenticated) {
    return <div>Loading...</div>
  }

  return (
    <main className="flex h-screen bg-white">
      {/* Sidebar */}
      <aside className="w-64 border-r border-gray-200 bg-gray-50 p-4">
        <div className="mb-6">
          <button className="w-full px-4 py-2 bg-brand-600 text-white rounded-lg hover:bg-brand-700">
            New Chat
          </button>
        </div>
        <div className="space-y-2">
          <p className="text-sm text-gray-600">Recent conversations</p>
        </div>
      </aside>

      {/* Main chat area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="border-b border-gray-200 bg-white px-8 py-4 flex justify-between items-center">
          <h1 className="text-xl font-semibold text-gray-900">PersonalGPT</h1>
          <button className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg">
            Settings
          </button>
        </header>

        {/* Chat content */}
        <div className="flex-1 overflow-y-auto p-8">
          <div className="max-w-2xl mx-auto space-y-4">
            <p className="text-gray-600 text-center">
              Start a new conversation or select one from the sidebar
            </p>
          </div>
        </div>

        {/* Input area */}
        <div className="border-t border-gray-200 bg-white px-8 py-4">
          <div className="max-w-2xl mx-auto flex gap-4">
            <input
              type="text"
              placeholder="Type your message here..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-brand-600 focus:border-transparent"
            />
            <button className="px-6 py-2 bg-brand-600 text-white rounded-lg hover:bg-brand-700">
              Send
            </button>
          </div>
        </div>
      </div>
    </main>
  )
}
