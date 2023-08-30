import uuid
from werkzeug.security import generate_password_hash

from Exceptions.exceptions import NotFoundException, ValidationFieldsException
from Models.user import User


class UserService:
    _user = None
    _data = None

    def create_user(self, current_user=None):
        name, email, role, country = self.data.get('name'), self.data.get('email'), self.data.get(
            'role'), self.data.get('country')
        password = self.data.get('password')

        if not current_user or current_user.role != User.ADMIN:
            role = User.USER

        if not all([name, email, role, country, password]):
            raise ValidationFieldsException('Name, role, email and password are mandatory.')

        user = User.get_user_by_email(email)
        if not user:
            # database ORM object
            self.user = User(
                public_id=str(uuid.uuid4()),
                name=name,
                email=email,
                role=role,
                budget=User.INITIAL_BUDGET,
                country=country,
                password=generate_password_hash(password)
            )
        else:
            raise ValidationFieldsException('User already exists. Please Log in.')

    def update_user(self):
        if not self.user:
            raise NotFoundException('User does not exist')

        name, email, role, country = self.data.get('name'), self.data.get('email'), self.data.get(
            'role'), self.data.get('country')
        password = self.data.get('password')

        if not any([name, email, role, country, password]):
            raise ValidationFieldsException('At least one of Name, role, email, country or password is mandatory.')

        if name:
            self.user.name = name
        if email:
            self.user.email = email
        if role:
            self.user.role = role
        if country:
            self.user.country = country
        if password:
            self.user.password = generate_password_hash(password)

    def update_my_profile(self):
        if not self.user:
            raise NotFoundException('User does not exist')

        name, country = self.data.get('name'), self.data.get('country')
        password = self.data.get('password')

        if not any([name, country, password]):
            raise ValidationFieldsException('At least one of Name, country or password is mandatory.')

        if name:
            self.user.name = name
        if country:
            self.user.country = country
        if password:
            self.user.password = generate_password_hash(password)

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data
