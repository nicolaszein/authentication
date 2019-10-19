from dataclasses import dataclass


@dataclass
class User:
    id: str
    full_name: str
    email: str

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email
        }
