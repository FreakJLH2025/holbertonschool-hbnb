from app import db
from app.models.base_model import BaseModel
from app.models.amenity import place_amenity

class Place(BaseModel):
    __tablename__ = 'places'

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False, default=0.0)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    reviews = db.relationship(
        'Review',
        backref='place',
        lazy=True,
        cascade='all, delete-orphan'
    )

    amenities = db.relationship(
        'Amenity',
        secondary=place_amenity,
        lazy='subquery',
        backref=db.backref('places', lazy=True)
    )

    def __init__(
        self,
        name,
        description,
        owner,
        price=0.0,
        latitude=None,
        longitude=None
    ):

        if not name:
            raise ValueError("Place must have a name")

        if price < 0:
            raise ValueError("Price must be non-negative")

        if latitude is not None and (latitude < -90 or latitude > 90):
            raise ValueError("Latitude must be between -90 and 90")

        if longitude is not None and (longitude < -180 or longitude > 180):
            raise ValueError("Longitude must be between -180 and 180")

        super().__init__()

        self.name = name
        self.description = description
        self.owner_id = owner.id
        self.price = price
        self.latitude = latitude
        self.longitude = longitude

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,

            "amenities": [
                a.to_dict() for a in self.amenities
            ],

            "reviews": [
                {
                    "id": r.id,
                    "text": r.text,
                    "rating": r.rating,
                    "user_id": r.user_id
                    
                }
                for r in self.reviews
            ],

            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
