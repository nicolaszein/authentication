from dataclasses import dataclass


@dataclass
class TokenData:
    id: str
    full_name: str
    email: str
    session_id: str = None

    def to_dict(self):
        data = {
            'id': str(self.id),
            'full_name': self.full_name,
            'email': self.email
        }

        if self.session_id:
            data['session_id'] = str(self.session_id)

        return data
