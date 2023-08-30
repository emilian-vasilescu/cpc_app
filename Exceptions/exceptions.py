class AccessDeniedException(Exception):

    def __init__(self, role, message="You don't have permissions", code=403):
        self.role = role
        self.message = message
        self.code = code
        super().__init__(self.message)


class NotFoundException(Exception):
    def __init__(self, message="Resource not found!", code=404):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ValidationFieldsException(Exception):
    def __init__(self, message="Submitted fields are wrong!", code=400):
        self.message = message
        self.code = code
        super().__init__(self.message)


class AuthenticationException(Exception):
    def __init__(self, message="Authentication denied!", code=401):
        self.message = message
        self.code = code
        super().__init__(self.message)
