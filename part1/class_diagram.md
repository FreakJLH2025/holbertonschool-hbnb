classDiagram
class User {
    +UUID id
    +String firstName
    +String lastName
    +String email
    +String password
    +Boolean isAdmin
    +DateTime createdAt
    +DateTime updatedAt
    +create()
    +update()
    +delete()
    +list()
}

class Place {
    +UUID id
    +String title
    +String description
    +Float price
    +Float latitude
    +Float longitude
    +DateTime createdAt
    +DateTime updatedAt
    +create()
    +update()
    +delete()
    +list()
}

class Review {
    +UUID id
    +Integer rating
    +String comment
    +DateTime createdAt
    +DateTime updatedAt
    +create()
    +update()
    +delete()
    +list()
}

class Amenity {
    +UUID id
    +String name
    +String description
    +DateTime createdAt
    +DateTime updatedAt
    +create()
    +update()
    +delete()
    +list()
}

User "1" --> "many" Place : owns
User "1" --> "many" Review : writes
Place "1" --> "many" Review : has
Place "many" --> "many" Amenity : includes