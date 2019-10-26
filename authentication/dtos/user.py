from dataclasses import dataclass


@dataclass
class User:
    id: str
    full_name: str
    email: str

    @classmethod
    def from_user_model(cls, user):
        return cls(id=str(user.id), full_name=user.full_name, email=user.email)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email
        }
