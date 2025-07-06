from .BaseModel import BaseModel
import re
from app.extensions import db, bcrypt


class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
      super().__init__()
      if not first_name or not last_name or not email:
          raise ValueError("First name, last name, and email are required.")
      if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
          raise ValueError("Invalid email format.")
      self.first_name = first_name
      self.last_name = last_name
      self.email = email
      self.is_admin = is_admin
      
    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)