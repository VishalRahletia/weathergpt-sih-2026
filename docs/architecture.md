# Architecture
```mermaid
flowchart LR
 UI[React responsive UI] --> API[FastAPI]
 API --> GEO[Location resolver]
 API --> P[Provider abstraction]
 P --> OM[Open-Meteo live]
 P --> M[Deterministic mock fallback]
 API --> N[Normalized schemas + freshness validation]
 N --> R[Deterministic risk rules]
 N --> C[Grounded response composer]
 R --> C
 API -. optional .-> PG[(PostgreSQL)]
 API -. optional .-> REDIS[(Redis cache)]
```
The database and Redis services are included in Compose for persistent history, subscriptions, and caching. This MVP holds those records in memory until repository wiring is enabled; it does not falsely claim persistence.
