class UserNotFoundException(Exception):
    """
    Raised when a user is not found in the database.
    """
    def __init__(self, message: str = "User not found"):
        self.message = message
        super().__init__(self.message)

class UserAlreadyExistsException(Exception):
    """
    Raised when a user with the same email already exists.
    """
    def __init__(self, message: str = "User already exists"):
        self.message = message
        super().__init__(self.message)

class UserNotActiveException(Exception):
    """
    Raised when a user is not active.
    """
    def __init__(self, message: str = "User is not active"):
        self.message = message
        super().__init__(self.message)