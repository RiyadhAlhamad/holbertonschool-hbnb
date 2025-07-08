from app.models.amenity import Amenity
from app.services.repositories import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)