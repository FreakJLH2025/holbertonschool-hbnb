sequenceDiagram
    participant Client
    participant API
    participant BusinessLogic
    participant Database

    Client->>API: POST /reviews (review data)
    API->>BusinessLogic: Validate User and Place
    BusinessLogic->>BusinessLogic: Create Review object
    BusinessLogic->>Database: Save Review
    Database-->>BusinessLogic: Confirmation
    BusinessLogic-->>API: Review created response
    API-->>Client: 201 Created (Review object)