import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app import create_app, db
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place

app = create_app('development')

with app.app_context():
    db.create_all()

    # CREATE ADMIN
    admin = User.query.filter_by(email='admin@hbnb.io').first()

    if not admin:
        admin = User(
            first_name='Admin',
            last_name='HBnB',
            email='admin@hbnb.io',
            password='admin1234',
            is_admin=True
        )

        db.session.add(admin)
        db.session.commit()

        print(f"Admin created with id: {admin.id}")

    else:
        print("Admin already exists")

    # CREATE AMENITIES
    amenities = ['WiFi', 'Swimming Pool', 'Air Conditioning']

    for name in amenities:

        if not Amenity.query.filter_by(name=name).first():

            amenity = Amenity(name=name)

            db.session.add(amenity)

            print(f"Amenity created: {name}")

        else:
            print(f"Amenity already exists: {name}")

    db.session.commit()

    # GET AMENITIES
    wifi = Amenity.query.filter_by(name='WiFi').first()
    pool = Amenity.query.filter_by(name='Swimming Pool').first()
    ac = Amenity.query.filter_by(name='Air Conditioning').first()

    # CREATE PLACES
    places = [
        {
            "name": "Beach House",
            "description": "Beautiful beach house with ocean view",
            "price": 120.0
        },
        {
            "name": "Mountain Cabin",
            "description": "Cozy cabin in the mountains",
            "price": 80.0
        },
        {
            "name": "City Apartment",
            "description": "Modern apartment downtown",
            "price": 150.0
        }
    ]

    for p in places:

        existing_place = Place.query.filter_by(name=p["name"]).first()

        if existing_place:
            print(f"Place already exists: {p['name']}")
            continue

        place = Place(
            p["name"],
            p["description"],
            admin,
            p["price"],
            None,
            None
        )

        place.amenities.append(wifi)
        place.amenities.append(pool)
        place.amenities.append(ac)

        db.session.add(place)

        print(f"Place created: {p['name']}")

    db.session.commit()

    print("Done!")