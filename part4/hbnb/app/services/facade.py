from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.services.repositories.user_repository import UserRepository


class HBnBFacade:
    def __init__(self):
        self.user_repository = UserRepository()
        self.place_repository = SQLAlchemyRepository(Place)
        self.review_repository = SQLAlchemyRepository(Review)
        self.amenity_repository = SQLAlchemyRepository(Amenity)

    ### Users section###

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repository.add(user)
        return user

    def get_user_by_id(self, user_id):
        return self.user_repository.get(user_id)

    def get_all_users(self):
        return self.user_repository.get_all()

    def get_user_by_email(self, email):
        return self.user_repository.get_by_attribute('email', email)

    def put_user(self, user_id, user_data):
        user = self.user_repository.get(user_id)
        if user:
            user.update(user_data)
            self.user_repository.update(user_id, user_data)
            return user
        return None

    ### Amenity section###

    def create_amenity(self, amenity_data):
        name = amenity_data.get("name", "")
        new_amenity = Amenity(name=name)
        self.amenity_repository.add(new_amenity)
        return new_amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repository.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repository.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repository.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)
            self.amenity_repository.update(amenity_id, amenity_data)
            return amenity
        return None

    ### Place section###

    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        if not owner_id:
            raise ValueError("Owner ID is required")
        owner = self.user_repository.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        amenity_ids = place_data.get('amenities', [])
        amenities = []
        for amenity_id in amenity_ids:
            amenity = self.amenity_repository.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity {amenity_id} not found")
            amenities.append(amenity)

        try:
            place = Place(
                title=place_data['title'],
                description=place_data.get('description', ''),
                price=place_data['price'],
                latitude=place_data['latitude'],
                longitude=place_data['longitude'],
                owner=owner
            )
        except ValueError as e:
            raise ValueError(str(e))

        for amenity in amenities:
            place.add_amenity(amenity)

        self.place_repository.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repository.get(place_id)
        if not place:
            raise ValueError("Place not found.")
        return place

    def get_all_places(self):
        return self.place_repository.get_all()

    def update_place(self, place_id, data):
        place = self.place_repository.get(place_id)
        if not place:
            return None
        if "owner_id" in data:
            new_owner = self.user_repository.get(data["owner_id"])
            if not new_owner:
                raise ValueError("Owner not found.")
            place.owner = new_owner
            data.pop("owner_id")
        if "amenities" in data:
            updated_amenities = []
            for amenity_id in data["amenities"]:
                amenity_obj = self.amenity_repository.get(amenity_id)
                if amenity_obj:
                    updated_amenities.append(amenity_obj)
            place.amenities = updated_amenities
            data.pop("amenities")

        place.update(data)
        self.place_repository.update(place_id, data)
        return place

    ### Review section###

    def create_review(self, review_data):
        user = self.user_repository.get(review_data["user_id"])
        if not user:
            raise ValueError("User not found.")

        place = self.place_repository.get(review_data["place_id"])
        if not place:
            raise ValueError("Place not found.")

        new_review = Review(
            text=review_data["text"],
            rating=review_data["rating"],
            user=user,
            place=place
        )
        self.review_repository.add(new_review)
        place.add_review(new_review)
        self.place_repository.update(place.id, {"reviews": place.reviews})
        return new_review

    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        review = self.review_repository.get(review_id)
        if not review:
            raise ValueError("Review not found")
        return review

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        return self.review_repository.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repository.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return [
            review for review in self.review_repository.get_all()
            if review.place.id == place_id
        ]

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        try:
            update_review = self.review_repository.get(review_id)
            update_review.update(review_data)
            self.review_repository.update(review_id, review_data)
            return update_review
        except Exception as e:
            raise ValueError(f"Error updating review: {str(e)}")

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        try:
            self.review_repository.delete(review_id)      
            return {"message": "Review deleted successfully"} 
        except ValueError:
                raise ValueError("Review not found")
