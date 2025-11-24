# Bingo Project

A **console-based 3×5 Bingo game** built entirely in Python with Docker containerization.
Players can fill their own cards, draw random numbers, and earn points for completing lines or diagonals.
Developed as part of the **Project Session 2** assignment.

## Features

✅ 3×5 Bingo Card — generated randomly or filled manually by the player  
✅ Duplicate Validation — prevents repeated numbers when entering custom cards  
✅ Automatic Marking — drawn numbers are automatically crossed off  
✅ Scoring System
- +10 pts per completed line
- +50 pts for full bingo (all 3 lines)
✅ Real-Time Updates — card and score refresh after each draw  
✅ Modular Structure — separated into src/game and src/ui folders for clarity  
✅ **Docker Containerization** — fully containerized with Docker Compose  
✅ **Redis Integration** — persistent storage for game history and high scores  
✅ **Custom Networking** — isolated Docker network for service communication  
✅ **Data Persistence** — volumes for Redis data persistence  

## File Structure

```
Bingo-Project/
├── README.md               # Project documentation
├── ARCHITECTURE.md         # Architecture documentation
├── DOCKER.md               # Docker setup and usage
├── TESTING.md              # Testing documentation
├── Makefile                # Build and test automation
├── pytest.ini              # Pytest configuration
├── docker-compose.yml      # Multi-service Docker configuration
├── bingo-game/
│   ├── Dockerfile          # Docker image definition
│   ├── .dockerignore       # Files excluded from Docker build
│   ├── main.py             # Application entry point
│   ├── requirements.txt    # Python dependencies
│   └── src/
│       ├── game/
│       │   ├── card.py     # Card generation & marking logic
│       │   ├── draw.py     # Random number drawing
│       │   ├── check.py    # Line, diagonal & bingo detection
│       │   └── score.py    # Scoring and Redis integration
│       └── ui/
│           └── terminal.py # Terminal input/output
└── tests/                  # Unit tests
    ├── conftest.py         # Pytest configuration and fixtures
    ├── requirements.txt    # Test dependencies
    ├── README.md           # Test documentation
    ├── test_card.py        # Card module tests
    ├── test_check.py       # Check module tests
    ├── test_draw.py        # Draw module tests
    └── test_score.py       # Score module tests
```

## Docker Architecture

This project demonstrates Docker best practices:

- **Multi-service Architecture**: Bingo game and Redis services
- **Custom Network**: Isolated bridge network for service communication
- **Volumes**: Persistent storage for Redis data
- **Environment Variables**: Configurable Redis connection
- **Health Checks**: Service health monitoring
- **Layer Optimization**: Efficient Dockerfile with proper caching
- **Security**: Non-root user in containers

## Prerequisites

- **Docker** (version 20.10 or higher)
- **Docker Compose** (version 2.0 or higher)

To verify installation:
```bash
docker --version
docker compose version
```

## Quick Start with Docker (Recommended)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/oscarthesade/Bingo-Project.git
cd Bingo-Project
```

### 2️⃣ Start the application
```bash
docker compose up
```
In a new terminal run:
```bash
docker compose exec -it bingo-game python main.py
```

These commands will:
- Build the Bingo game Docker image
- Start Redis service with persistent storage
- Create a custom Docker network
- Launch the Bingo game container

### 3️⃣ Play the game!
- Choose to create your own card or get a random one
- Press Enter each round to draw a new number
- Watch your card fill and your score increase
- High scores are automatically saved to Redis

### 4️⃣ Stop the application
```bash
docker compose down
```

To also remove volumes (clears Redis data):
```bash
docker compose down -v
```

## Docker Commands Reference

### Build and Run
```bash
# Build and start all services
docker compose up

# Build and start in detached mode (background)
docker compose up -d

# Rebuild images before starting
docker compose up --build

# View logs
docker compose logs -f

# View logs for specific service
docker compose logs -f bingo-game
```

### Service Management
```bash
# Stop services
docker compose stop

# Start stopped services
docker compose start

# Restart services
docker compose restart

# Remove containers and networks
docker compose down

# Remove everything including volumes
docker compose down -v
```

### Container Interaction
```bash
# Execute command in running container
docker compose exec bingo-game python -c "print('Hello')"

# Access Redis CLI
docker compose exec redis redis-cli

# View Redis data
docker compose exec redis redis-cli GET high_score
docker compose exec redis redis-cli LRANGE game_history 0 -1
```

### Docker Image Management
```bash
# Build image manually
docker build -t bingo-game:latest ./bingo-game

# View Docker images
docker images

# View container status
docker compose ps

# Inspect network
docker network inspect bingo-project_bingo-network
```

## Running Without Docker (Local Development)

### 1️⃣ Clone the repository
```bash
git clone https://github.com/oscarthesade/Bingo-Project.git
cd Bingo-Project/bingo-game
```

### 2️⃣ Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate   # On Mac/Linux
# or
venv\Scripts\activate       # On Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the game
```bash
python main.py
```

**Note**: Without Docker, Redis features (high scores, game history) will be unavailable, but the game will still function.

## Scoring System

| Event                    | Points |
|-------------------------|--------|
| Completing a line       | +10    |
| Full bingo (3 lines)    | +50    |

## Docker Configuration Details

### Dockerfile Features
- **Base Image**: Python 3.10-slim for optimized size
- **Layer Caching**: Requirements installed before code copy for better caching
- **Security**: Non-root user (UID 1000) for container security
- **Health Check**: Container health monitoring
- **Environment Variables**: Configurable Redis connection

### Docker Compose Services

#### `bingo-game` Service
- **Build Context**: `./bingo-game`
- **Network**: Custom `bingo-network`
- **Dependencies**: Waits for Redis health check
- **Environment**: Redis host and port configuration
- **Interactive**: Supports stdin/tty for user input

#### `redis` Service
- **Image**: `redis:alpine` (lightweight)
- **Port**: 6379 (exposed to host)
- **Volume**: `redis-data` for persistent storage
- **Persistence**: AOF (Append Only File) enabled
- **Health Check**: Redis ping command

### Network Architecture
- **Network Type**: Bridge (default)
- **Network Name**: `bingo-network`
- **Service Discovery**: Containers can communicate by service name

### Volume Management
- **Volume Name**: `redis-data`
- **Purpose**: Persist Redis data across container restarts
- **Location**: Managed by Docker at `/var/lib/docker/volumes/`

## Environment Variables

The application supports the following environment variables:

| Variable     | Default | Description                    |
|--------------|---------|--------------------------------|
| `REDIS_HOST` | `redis` | Redis service hostname         |
| `REDIS_PORT` | `6379`  | Redis service port             |
| `DEBUG`      | `false` | Enable debug logging           |

Set environment variables in `docker-compose.yml` or via command line:
```bash
docker compose run -e DEBUG=true bingo-game
```

## Troubleshooting

### Redis Connection Issues
If you see Redis connection errors:
1. Verify Redis container is running: `docker compose ps`
2. Check Redis logs: `docker compose logs redis`
3. Test Redis connection: `docker compose exec redis redis-cli ping`

### Container Won't Start
1. Check Docker daemon is running: `docker ps`
2. Verify Docker Compose version: `docker compose version`
3. Rebuild images: `docker compose build --no-cache`

### Port Already in Use
If port 6379 is already in use:
1. Change port mapping in `docker-compose.yml`:
   ```yaml
   ports:
     - "6380:6379"  # Use 6380 on host instead
   ```

## Contributors
- Clement Standaert
- Oscar Thiele
- Arthur Hennessy
- Max Goldenberg
- Luis Schaefer
- Nadim Bteish

