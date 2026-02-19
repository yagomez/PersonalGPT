# PersonalGPT Docker Setup

This directory contains Docker configurations for PersonalGPT.

## Files

- `Dockerfile.backend` — FastAPI backend container
- `Dockerfile.frontend` — Next.js frontend container
- `docker-compose.yml` — Full-stack orchestration (in project root)

## Running with Docker Compose

### Quick Start

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Remove volumes (reset database)
docker-compose down -v
```

### Individual Services

```bash
# Start just backend
docker-compose up -d backend

# Start just frontend
docker-compose up -d frontend

# Start just database
docker-compose up -d postgres
```

## Services

| Service | Port | Purpose |
|---------|------|---------|
| Frontend | 3000 | Next.js React app |
| Backend | 8000 | FastAPI server |
| Postgres | 5432 | Primary database |
| Redis | 6379 | Cache layer |
| Chroma | 8001 | Vector database |

## Environment Variables

Create `.env` file in project root:

```bash
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-your-key-here
```

## Access Points

- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Chroma: http://localhost:8001

## Database

Database credentials:
- User: `personalgpt`
- Password: `personalgpt`
- Database: `personalgpt`

Connect directly:
```bash
psql -h localhost -U personalgpt -d personalgpt
```

## Troubleshooting

### Port already in use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Database connection error
```bash
# Check database is running
docker-compose ps postgres

# View database logs
docker-compose logs postgres
```

### Rebuild images
```bash
# Remove old images
docker-compose down --rmi all

# Rebuild
docker-compose up --build
```

## Development

### Backend Development

```bash
# Shell into backend
docker-compose exec backend bash

# Run migrations
docker-compose exec backend alembic upgrade head

# Run tests
docker-compose exec backend pytest
```

### Frontend Development

```bash
# Shell into frontend
docker-compose exec frontend sh

# Install packages
docker-compose exec frontend npm install
```

## Production Build

```bash
# Build optimized images
docker-compose -f docker-compose.yml build --no-cache

# Run in production mode
docker-compose -f docker-compose.yml up
```
