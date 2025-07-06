from .BaseModel import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        if not text or len(text) > 1024:
            raise ValueError("Review text must be non-empty and ≤ 1024 characters.")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        if not place or not user:
            raise ValueError("Place and User are required and must be valid objects.")
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user