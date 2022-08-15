from core.clients.api_client import ApiClient
from core.models.users import CreateUserModel


class User:
    def __init__(self, create_user_model: CreateUserModel):
        self.api = ApiClient()
        self.token = None

        self.username = create_user_model.username
        self.password = create_user_model.password
        self.firstname = create_user_model.firstname
        self.lastname = create_user_model.lastname
        self.phone = create_user_model.phone
        self.api.register(json_data=create_user_model.dict())

    @staticmethod
    def create_without_login():
        return User(CreateUserModel.create())

    @staticmethod
    def create():
        user = User(CreateUserModel.create())
        user.login()
        return user

    def login(self):
        self.token = self.api.login(username=self.username, password=self.password).token
        self.api.token = self.token
