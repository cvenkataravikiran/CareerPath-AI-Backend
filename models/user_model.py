# models/user_model.py
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, name, email, password, public_id=None, created_at=None, _id=None):
        self.public_id = public_id or str(uuid.uuid4())
        self.name = name
        self.email = email
        self.password = generate_password_hash(password) if password else None
        self.created_at = created_at
        self._id = _id

    def to_dict(self):
        return {
            "public_id": self.public_id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at,
            "_id": str(self._id) if self._id else None
        }

    @staticmethod
    def from_dict(data):
        return User(
            name=data.get("name"),
            email=data.get("email"),
            password=data.get("password"),
            public_id=data.get("public_id"),
            created_at=data.get("created_at"),
            _id=data.get("_id")
        )

    def check_password(self, password):
        return check_password_hash(self.password, password)