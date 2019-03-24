import bcrypt


class Authentication:

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    @staticmethod
    def validate_password(password, hashed_password):
        return bcrypt.checkpw(password.encode(), hashed_password)
