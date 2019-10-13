class ValidatorError(Exception):
    def __init__(self, message, errors):
        super()

        self.errors = errors
