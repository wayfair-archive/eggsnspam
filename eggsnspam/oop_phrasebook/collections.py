from .daos import BreakfastDao, IngredientDao, UserDao, UserPreferenceDao
from .models import BreakfastModel, IngredientModel, UserModel, UserPreferenceModel


class BaseCollection(object):

    DEFAULT_DAO = None
    MODEL = None

    def __init__(self, dao=None):
        if dao is None:
            dao = self.DEFAULT_DAO()
        self.dao = dao
        self.models = []

    def create_model(self, data):
        """Instantiate and populate a model from the provided data"""
        obj = self.MODEL(dao=self.dao)
        obj.populate(data)
        return obj

    def populate(self, data_set):
        """Instantiate multiple models from a set of data"""
        self.models = [self.create_model(d) for d in data_set]


class BreakfastCollection(BaseCollection):

    DEFAULT_DAO = BreakfastDao
    MODEL = BreakfastModel

    def load_all(self):
        """Load all the records from the database"""
        self.populate(self.dao.list_all())
        return True


class IngredientCollection(BaseCollection):

    DEFAULT_DAO = IngredientDao
    MODEL = IngredientModel

    def load_all(self):
        """Load all the records from the database"""
        self.populate(self.dao.list_all())
        return True


class UserCollection(BaseCollection):

    DEFAULT_DAO = UserDao
    MODEL = UserModel

    def load_all(self):
        """Load all the records from the database"""
        self.populate(self.dao.list_all())
        return True


class UserPreferenceCollection(BaseCollection):

    DEFAULT_DAO = UserPreferenceDao
    MODEL = UserPreferenceModel

    def load_all_for_user(self, user_id):
        """Load all the records from the database"""
        self.populate(self.dao.list_all_for_user(user_id))
        return True
