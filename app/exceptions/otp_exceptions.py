class InvalidOtpException(Exception):
    """
    Raised when a user is not found in the database.
    """
    def __init__(self, message: str = "User not found"):
        self.message = message
        super().__init__(self.message)
