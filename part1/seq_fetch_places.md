sequenceDiagram
    participant Client
    participant API
    participant BusinessLogic
    participant Database

    Client->>API: GET /places?criteria=...
    API->>BusinessLogic: Request list of Places
    BusinessLogic->>Database: Query Places with criteria
    Database-->>BusinessLogic: Return list of Places
    BusinessLogic-->>API: Format and return data
    API-->>Client: 200 OK (List of Places)