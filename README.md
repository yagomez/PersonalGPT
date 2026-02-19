# PersonalGPT

A full-stack personalized AI assistant with browser integration, built with modern web and AI technologies.

## Stack Overview

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js, React, Tailwind CSS |
| Backend API | FastAPI (Python) |
| AI Orchestration | LangChain |
| LLM Providers | OpenAI / Claude / Gemini |
| Relational DB | PostgreSQL (+ pgvector) |
| Vector Store | Chroma |
| Cache / Memory | Redis |
| Auth | JWT / Supabase Auth |
| Deployment | Docker + Vercel/Render |
| Future | Browser Extension (Manifest v3) |

## Project Structure

```
PersonalGPT/
├── frontend/           # Next.js React application
├── backend/            # FastAPI Python backend
├── docs/              # Project documentation
├── docker/            # Docker configurations
├── extension/         # Browser extension (future)
└── .github/workflows/ # CI/CD pipelines
```

## Quick Start

See [GETTING_STARTED.md](docs/GETTING_STARTED.md) for setup instructions.

## Documentation

- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design & component flow
- [DEVELOPMENT.md](docs/DEVELOPMENT.md) - Development guidelines
- [API.md](docs/API.md) - Backend API documentation
- [ROADMAP.md](ROADMAP.md) - Project timeline & phases

## License

MIT
