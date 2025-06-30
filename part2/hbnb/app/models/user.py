from .BaseModel import BaseModel
import re
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
      
