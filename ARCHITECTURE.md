# Bingo Project Architecture

## Docker Architecture Diagram

```mermaid
graph TB
    subgraph "Docker Host"
        subgraph "bingo-network (Bridge Network)"
            subgraph "bingo-game Container"
                APP[Python Application<br/>main.py]
                SCORE[ScoreTracker<br/>Redis Client]
                APP --> SCORE
            end
            
            subgraph "redis Container"
                REDIS[(Redis Server<br/>Port 6379)]
                AOF[Append Only File<br/>AOF Persistence]
                REDIS --> AOF
            end
            
            SCORE <-->|TCP:6379<br/>Service Discovery| REDIS
        end
        
        subgraph "Docker Volumes"
            VOL[redis-data Volume<br/>Persistent Storage]
            AOF -.->|Mounted at /data| VOL
        end
        
        subgraph "Host Machine"
            USER[User Terminal]
            HOST_PORT[Host Port 6379]
        end
        
        USER -->|docker compose exec| APP
        HOST_PORT <-->|Port Mapping| REDIS
    end
    
    style APP fill:#4a90e2,stroke:#2c5aa0,color:#fff
    style REDIS fill:#dc382d,stroke:#a02820,color:#fff
    style VOL fill:#28a745,stroke:#1e7e34,color:#fff
    style SCORE fill:#6c757d,stroke:#545b62,color:#fff
```

## Component Details

### Containers

**bingo-game Container:**
- **Image**: Custom built from `bingo-game/Dockerfile`
- **Base**: `python:3.10-slim`
- **User**: Non-root (`bingo`, UID 1000)
- **Health Check**: Python process check every 30s
- **Dependencies**: Waits for Redis health check

**redis Container:**
- **Image**: `redis:alpine`
- **Port**: 6379 (exposed to host)
- **Persistence**: AOF (Append Only File) enabled
- **Health Check**: `redis-cli ping` every 10s
- **Volume**: `/data` mounted to `redis-data`

### Network

**bingo-network:**
- **Type**: Bridge network
- **Purpose**: Isolated container communication
- **Service Discovery**: Containers resolve by service name
- **Internal Communication**: No port mapping required

### Data Flow

1. **Game Initialization:**
   ```
   User → docker compose exec → bingo-game container
   → ScoreTracker initializes → Connects to Redis
   ```

2. **Gameplay:**
   ```
   Game logic → Score calculation → Redis storage
   → Volume persistence → Data survives restarts
   ```

3. **High Score Retrieval:**
   ```
   Game start → Redis query → High score display
   ```

## Deployment Sequence

```mermaid
sequenceDiagram
    participant User
    participant DockerCompose
    participant Redis
    participant BingoGame
    participant Volume

    User->>DockerCompose: docker compose up
    DockerCompose->>Redis: Start container
    Redis->>Volume: Mount redis-data
    Redis->>Redis: Health check (ping)
    Redis-->>DockerCompose: Healthy
    DockerCompose->>BingoGame: Start container (after Redis healthy)
    BingoGame->>Redis: Connect via service name
    Redis-->>BingoGame: Connection established
    BingoGame-->>User: Game ready
    User->>BingoGame: Play game
    BingoGame->>Redis: Store scores
    Redis->>Volume: Persist data
```

## Service Dependencies

```mermaid
graph LR
    A[docker compose up] --> B[Redis Container]
    B --> C{Health Check}
    C -->|Healthy| D[Bingo Game Container]
    C -->|Unhealthy| E[Wait & Retry]
    E --> C
    D --> F[Game Ready]
    
    style B fill:#dc382d,color:#fff
    style D fill:#4a90e2,color:#fff
    style C fill:#ffc107,color:#000
```

