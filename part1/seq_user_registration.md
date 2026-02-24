Sequence Diagram - User Registration

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant BusinessLogic
    participant Database

    Client->>API: POST /users/register (user data)
    API->>BusinessLogic: Validate and create User
    BusinessLogic->>Database: Save User
    Database-->>BusinessLogic: Confirmation
    BusinessLogic-->>API: User created response
    API-->>Client: 201 Created (User object)
