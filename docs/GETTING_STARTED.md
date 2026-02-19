# Getting Started

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- Redis 7+
- Git

## Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload
```

Server runs on `http://localhost:8000`

## Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Setup environment variables
cp .env.example .env.local

# Start development server
npm run dev
```

Frontend runs on `http://localhost:3000`

## Database Setup

```bash
# Create PostgreSQL database
createdb personalgpt

# Create Redis instance (Docker)
docker run -d -p 6379:6379 redis:latest

# Create Chroma collection (via Python)
python backend/scripts/init_chroma.py
```

## Configuration

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost/personalgpt
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=sk-...
JWT_SECRET=your-secret-key
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Running the Full Stack

### Option 1: Docker Compose

```bash
docker-compose up -d
```

### Option 2: Manual

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - Redis (if not containerized):**
```bash
redis-server
```

## Verification

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Next Steps

1. Read [ARCHITECTURE.md](ARCHITECTURE.md) for system design
2. Check [API.md](API.md) for backend endpoints
3. See [DEVELOPMENT.md](DEVELOPMENT.md) for coding standards
