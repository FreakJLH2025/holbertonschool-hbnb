sequenceDiagram
    participant Client
    participant API
    participant BusinessLogic
    participant Database

    Client->>API: POST /places (place data)
    API->>BusinessLogic: Validate and create Place
    BusinessLogic->>Database: Save Place
    Database-->>BusinessLogic: Confirmation
    BusinessLogic-->>API: Place created response
    API-->>Client: 201 Created (Place object)
