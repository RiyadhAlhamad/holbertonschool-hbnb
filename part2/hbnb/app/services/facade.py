from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

###Users section###

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def put_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if user:
            user.update(user_data)
            self.user_repo.update(user_id, user_data)
            return user
        return None

###Amenity section###

    def create_amenity(self, amenity_data):
        name = amenity_data.get("name", "")
        if not name or len(name) > 50:
            raise ValueError(
                "Invalid 'name': must be non-empty and ≤ 50 characters.")
        new_amenity = Amenity(name=name)
        self.amenity_repo.add(new_amenity)
        return new_amenity


    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)


    def get_all_amenities(self):
        return self.amenity_repo.get_all()


    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)
            self.amenity_repo.update(amenity_id, amenity_data)
            return amenity
        return None


###Place section###

    def create_place(self, place_data):
        if place_data["price"] < 0:
            raise ValueError("Price must be a non-negative value.")
        if not (-90 <= place_data["latitude"] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180 <= place_data["longitude"] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found.")

        place_new = Place(
            title=place_data["title"],
            description=place_data.get("description", ""),
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner=owner
        )
        if "amenities" in place_data:
            amenities = []
            for amenity_id in place_data["amenities"]:
                amenity_obj = self.amenity_repo.get(amenity_id)
                if amenity_obj:
                    amenities.append(amenity_obj)
            place_new.amenities = amenities

        self.place_repo.add(place_new)
        return place_new

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found.")
        return place

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
        if "price" in data and data["price"] < 0:
            raise ValueError("Price must be a non-negative value.")
        if "latitude" in data and not (-90 <= data["latitude"] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if "longitude" in data and not (-180 <= data["longitude"] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        if "owner_id" in data:
            new_owner = self.user_repo.get(data["owner_id"])
            if not new_owner:
                raise ValueError("Owner not found.")
            place.owner = new_owner
            data.pop("owner_id")
        if "amenities" in data:
            updated_amenities = []
            for amenity_id in data["amenities"]:
                amenity_obj = self.amenity_repo.get(amenity_id)
                if amenity_obj:
                    updated_amenities.append(amenity_obj)
            place.amenities = updated_amenities
            data.pop("amenities")

        place.update(data)
        self.place_repo.add(place)
        return place
    