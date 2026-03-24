from flask import request
from flask_restx import Namespace, Resource, fields
from facade.hbnb_facade import HBnBFacade
from business.user import User
from business.amenity import Amenity
from business.place import Place
from business.review import Review

facade = HBnBFacade()

# ---------------- USER ENDPOINTS ----------------
api_ns = Namespace("users", description="User operations")

user_model = api_ns.model("User", {
    "first_name": fields.String(required=True),
    "last_name": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True),
})

@api_ns.route("/")
class UserList(Resource):
    def get(self):
        return [u.to_dict() for u in facade.list_all() if isinstance(u, User)]

    @api_ns.expect(user_model)
    def post(self):
        data = request.json
        user = User(data["first_name"], data["last_name"], data["email"], data["password"])
        facade.create(user)
        return user.to_dict(), 201

@api_ns.route("/<string:user_id>")
class UserResource(Resource):
    def get(self, user_id):
        user = facade.get(user_id)
        if not user or not isinstance(user, User):
            return {"error": "User not found"}, 404
        return user.to_dict()

    @api_ns.expect(user_model)
    def put(self, user_id):
        user = facade.get(user_id)
        if not user or not isinstance(user, User):
            return {"error": "User not found"}, 404
        data = request.json
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.email = data.get("email", user.email)
        user.update()
        return user.to_dict(), 200


# ---------------- AMENITY ENDPOINTS ----------------
amenity_ns = Namespace("amenities", description="Amenity operations")

amenity_model = amenity_ns.model("Amenity", {
    "name": fields.String(required=True),
})

@amenity_ns.route("/")
class AmenityList(Resource):
    def get(self):
        return [a.to_dict() for a in facade.list_all() if isinstance(a, Amenity)]

    @amenity_ns.expect(amenity_model)
    def post(self):
        data = request.json
        amenity = Amenity(data["name"])
        facade.create(amenity)
        return amenity.to_dict(), 201

@amenity_ns.route("/<string:amenity_id>")
class AmenityResource(Resource):
    def get(self, amenity_id):
        amenity = facade.get(amenity_id)
        if not amenity or not isinstance(amenity, Amenity):
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict()

    @amenity_ns.expect(amenity_model)
    def put(self, amenity_id):
        amenity = facade.get(amenity_id)
        if not amenity or not isinstance(amenity, Amenity):
            return {"error": "Amenity not found"}, 404
        data = request.json
        amenity.name = data.get("name", amenity.name)
        amenity.update()
        return amenity.to_dict(), 200


# ---------------- PLACE ENDPOINTS ----------------
place_ns = Namespace("places", description="Place operations")

place_model = place_ns.model("Place", {
    "name": fields.String(required=True),
    "description": fields.String(required=True),
    "owner_id": fields.String(required=True),
    "price": fields.Float(required=False),
    "latitude": fields.Float(required=False),
    "longitude": fields.Float(required=False),
    "amenity_ids": fields.List(fields.String, required=False),
})

@place_ns.route("/")
class PlaceList(Resource):
    def get(self):
        return [p.to_dict() for p in facade.list_all() if isinstance(p, Place)]

    @place_ns.expect(place_model)
    def post(self):
        data = request.json
        owner = facade.get(data["owner_id"])
        if not owner or not isinstance(owner, User):
            return {"error": "Owner not found"}, 404

        place = Place(
            data["name"],
            data["description"],
            owner,
            data.get("price", 0.0),
            data.get("latitude"),
            data.get("longitude"),
        )

        amenity_ids = data.get("amenity_ids", [])
        for a_id in amenity_ids:
            amenity = facade.get(a_id)
            if amenity and isinstance(amenity, Amenity):
                place.amenities.append(amenity)

        facade.create(place)
        return place.to_dict(), 201

@place_ns.route("/<string:place_id>")
class PlaceResource(Resource):
    def get(self, place_id):
        place = facade.get(place_id)
        if not place or not isinstance(place, Place):
            return {"error": "Place not found"}, 404
        return place.to_dict()

    @place_ns.expect(place_model)
    def put(self, place_id):
        place = facade.get(place_id)
        if not place or not isinstance(place, Place):
            return {"error": "Place not found"}, 404
        data = request.json
        place.name = data.get("name", place.name)
        place.description = data.get("description", place.description)
        place.price = data.get("price", place.price)
        place.latitude = data.get("latitude", place.latitude)
        place.longitude = data.get("longitude", place.longitude)

        amenity_ids = data.get("amenity_ids")
        if amenity_ids is not None:
            place.amenities = []
            for a_id in amenity_ids:
                amenity = facade.get(a_id)
                if amenity and isinstance(amenity, Amenity):
                    place.amenities.append(amenity)

        place.update()
        return place.to_dict(), 200


# ---------------- REVIEW ENDPOINTS ----------------
review_ns = Namespace("reviews", description="Review operations")

review_model = review_ns.model("Review", {
    "text": fields.String(required=True),
    "rating": fields.Integer(required=True),
    "user_id": fields.String(required=True),
    "place_id": fields.String(required=True),
})

@review_ns.route("/")
class ReviewList(Resource):
    def get(self):
        return [r.to_dict() for r in facade.list_all() if isinstance(r, Review)]

    @review_ns.expect(review_model)
    def post(self):
        data = request.json
        user = facade.get(data["user_id"])
        place = facade.get(data["place_id"])
        if not user or not isinstance(user, User):
            return {"error": "User not found"}, 404
        if not place or not isinstance(place, Place):
            return {"error": "Place not found"}, 404

        review = Review(data["text"], data["rating"], user, place)
        facade.create(review)
        user.reviews.append(review)
        place.reviews.append(review)
        return review.to_dict(), 201

@review_ns.route("/<string:review_id>")
class ReviewResource(Resource):
    def get(self, review_id):
        review = facade.get(review_id)
        if not review or not isinstance(review, Review):
            return {"error": "Review not found"}, 404
        return review.to_dict()

    @review_ns.expect(review_model)
    def put(self, review_id):
        review = facade.get(review_id)
        if not review or not isinstance(review, Review):
            return {"error": "Review not found"}, 404
        data = request.json
        review.text = data.get("text", review.text)
        review.rating = data.get("rating", review.rating)
        review.update()
        return review.to_dict(), 200

    def delete(self, review_id):
        review = facade.get(review_id)
        if not review or not isinstance(review, Review):
            return {"error": "Review not found"}, 404
        if review in review.user.reviews:
            review.user.reviews.remove(review)
        if review in review.place.reviews:
            review.place.reviews.remove(review)
        facade.delete(review_id)
        return {"message": "Review deleted successfully"}, 200
