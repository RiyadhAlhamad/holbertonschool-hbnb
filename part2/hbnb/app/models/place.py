from .BaseModel import BaseModel
class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        if not title or len(title) > 100:
            raise ValueError("Invalid 'title': must be non-empty and ≤ 100 characters.")
        if not description or len(description) > 500:
            raise ValueError("Invalid 'description': must be non-empty and ≤ 500 characters.")
        if price < 0:
            raise ValueError("Invalid 'price': must be a non-negative value.")
        if not (-90 <= latitude <= 90):
            raise ValueError("Invalid 'latitude': must be between -90 and 90.")
        if not (-180 <= longitude <= 180):
            raise ValueError("Invalid 'longitude': must be between -180 and 180.")
        if not owner:
            raise ValueError("Owner is required and must be a valid User object.")
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  
        self.amenities = []  

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
