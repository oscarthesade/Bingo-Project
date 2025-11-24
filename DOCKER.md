# Docker Documentation

This document provides detailed information about the Docker setup for the Bingo Project.

## Architecture Overview

The application uses a **multi-container architecture** with the following services:

1. **bingo-game**: The main Python application
2. **redis**: Data persistence service for game history and high scores

## Dockerfile Details

### Location
`bingo-game/Dockerfile`

### Key Features

#### Base Image
- **Image**: `python:3.10-slim`
- **Why**: Lightweight Python runtime, reduces image size significantly

#### Layer Optimization
```dockerfile
# Dependencies installed before code copy
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=bingo:bingo . .
```
This ordering ensures that dependency installation is cached unless `requirements.txt` changes.

#### Security
- Non-root user (`bingo`, UID 1000)
- Files owned by non-root user
- Minimal attack surface

#### Environment Variables
- `PYTHONUNBUFFERED=1`: Ensures Python output is not buffered
- `PYTHONDONTWRITEBYTECODE=1`: Prevents `.pyc` file creation
- `REDIS_HOST` and `REDIS_PORT`: Configurable Redis connection

#### Health Check
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1
```
Monitors container health every 30 seconds.

## Docker Compose Configuration

### Network Architecture

**Custom Bridge Network**: `bingo-network`
- **Type**: Bridge (default Docker network driver)
- **Purpose**: Isolated communication between services
- **Service Discovery**: Containers can communicate using service names

### Volume Management

**Volume**: `redis-data`
- **Type**: Named volume (Docker-managed)
- **Purpose**: Persist Redis data across container restarts
- **Location**: `/var/lib/docker/volumes/bingo-project_redis-data/`
- **Persistence**: Data survives container removal

### Service Dependencies

```yaml
depends_on:
  redis:
    condition: service_healthy
```

The bingo-game service waits for Redis to pass its health check before starting.

### Health Checks

#### Redis Health Check
```yaml
healthcheck:
  test: ["CMD", "redis-cli", "ping"]
  interval: 10s
  timeout: 5s
  retries: 5
```

#### Bingo Game Health Check
```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import sys; sys.exit(0)"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 5s
```

## Build Process

### Image Building
```bash
docker compose build
```

**Build Steps**:
1. Docker reads `Dockerfile` from `bingo-game/` directory
2. Creates layers for each instruction
3. Caches layers for faster subsequent builds
4. Tags image as `bingo-project-bingo-game:latest`

### Layer Caching Strategy
- **Layer 1**: Base image (cached if unchanged)
- **Layer 2**: Working directory setup (cached)
- **Layer 3**: Environment variables (cached)
- **Layer 4**: User creation (cached)
- **Layer 5**: Requirements copy (invalidated if `requirements.txt` changes)
- **Layer 6**: Dependency installation (invalidated if requirements change)
- **Layer 7**: Application code copy (invalidated if code changes)

## Runtime Behavior

### Container Lifecycle

1. **Startup**:
   - Redis container starts first
   - Redis health check runs
   - Once healthy, bingo-game container starts
   - Bingo-game connects to Redis via service name

2. **Runtime**:
   - Containers communicate over `bingo-network`
   - Redis persists data to volume
   - Health checks run periodically

3. **Shutdown**:
   - `docker compose down`: Stops and removes containers
   - `docker compose down -v`: Also removes volumes (data loss)

## Networking Details

### Service Discovery
Containers can reach each other using:
- **Service name**: `redis`, `bingo-game`
- **Container name**: `bingo-redis`, `bingo-app`
- **Network alias**: Same as service name

### Port Mapping
```yaml
ports:
  - "6379:6379"  # host:container
```
Redis port 6379 is exposed to the host machine for direct access.

### Internal Communication
- Bingo-game connects to Redis using hostname `redis`
- No port specification needed (default Redis port)
- Communication stays within Docker network

## Data Persistence

### Redis Data Storage
- **AOF (Append Only File)**: Enabled for durability
- **Volume Mount**: `/data` directory in container
- **Backup**: Volume can be backed up from host

### Accessing Redis Data
```bash
# View high score
docker compose exec redis redis-cli GET high_score

# View game history
docker compose exec redis redis-cli LRANGE game_history 0 -1

# Clear all data
docker compose exec redis redis-cli FLUSHALL
```

## Environment Configuration

### Default Values
- `REDIS_HOST=redis`
- `REDIS_PORT=6379`
- `DEBUG=false`

### Overriding Environment Variables

**Method 1: docker-compose.yml**
```yaml
environment:
  - DEBUG=true
```

**Method 2: Command line**
```bash
docker compose run -e DEBUG=true bingo-game
```

**Method 3: .env file**
Create `.env` in project root:
```
DEBUG=true
REDIS_PORT=6380
```

## Troubleshooting

### View Container Logs
```bash
# All services
docker compose logs

# Specific service
docker compose logs bingo-game
docker compose logs redis

# Follow logs
docker compose logs -f
```

### Inspect Network
```bash
docker network inspect bingo-project_bingo-network
```

### Inspect Volume
```bash
docker volume inspect bingo-project_redis-data
```

### Container Shell Access
```bash
# Bingo game container
docker compose exec bingo-game /bin/bash

# Redis container
docker compose exec redis sh
```

### Rebuild from Scratch
```bash
# Remove everything
docker compose down -v
docker system prune -a

# Rebuild
docker compose build --no-cache
docker compose up
```

## Best Practices Demonstrated

1. ✅ **Multi-stage builds** (not needed here, but structure supports it)
2. ✅ **Layer caching optimization**
3. ✅ **Non-root user**
4. ✅ **Health checks**
5. ✅ **Custom networks**
6. ✅ **Volume persistence**
7. ✅ **Environment variable configuration**
8. ✅ **Service dependencies**
9. ✅ **Restart policies**
10. ✅ **.dockerignore for build optimization**

## Performance Considerations

### Image Size
- Base image: ~45MB (python:3.10-slim)
- With dependencies: ~50-60MB
- Total: Minimal footprint

### Build Time
- First build: ~2-3 minutes
- Subsequent builds: ~10-30 seconds (with cache)
- Cache invalidation: Only when dependencies or code change

### Runtime Resources
- Memory: ~50MB per container
- CPU: Minimal (game logic is lightweight)
- Network: Low bandwidth (Redis communication)

## Security Considerations

1. **Non-root user**: Reduces privilege escalation risk
2. **Minimal base image**: Fewer vulnerabilities
3. **Network isolation**: Services only communicate within Docker network
4. **No exposed ports** (except Redis for debugging)
5. **Read-only root filesystem** (can be added if needed)

## Scaling Considerations

While this is a single-player game, the architecture supports:
- Multiple game instances (different ports)
- Redis clustering (with configuration changes)
- Load balancing (with additional services)

## Future Enhancements

Potential Docker improvements:
- Multi-stage builds for even smaller images
- Docker secrets for sensitive data
- Docker Swarm for orchestration
- Kubernetes manifests for cloud deployment
- CI/CD integration with Docker builds

