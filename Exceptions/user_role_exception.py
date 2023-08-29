class UserRoleException(Exception):

    def __init__(self, role, message="You don't have permissions"):
        self.role = role
        self.message = message
        self.code = 403
        super().__init__(self.message)
