export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">PersonalGPT</h1>
        <p className="text-lg text-gray-600 mb-8">
          Your personalized AI assistant
        </p>
        <div className="flex gap-4 justify-center">
          <a
            href="/login"
            className="px-6 py-2 bg-brand-600 text-white rounded-lg hover:bg-brand-700"
          >
            Login
          </a>
          <a
            href="/register"
            className="px-6 py-2 border border-gray-300 text-gray-900 rounded-lg hover:bg-gray-50"
          >
            Sign Up
          </a>
        </div>
      </div>
    </main>
  )
}
