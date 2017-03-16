from eggsnspam.common.recommendations import dot_product

from .daos import BreakfastDao, IngredientDao, UserDao, UserPreferenceDao, BreakfastIngredientDao


def _validate_string(value):
    """Return True if value is a string and is not empty"""
    return value.__class__ in (str, unicode) and value


def _validate_int(value):
    """Return True if value is an integer"""
    return value.__class__ == int


def _validate_float(value):
    """Return True if value is an integer"""
    return value.__class__ in (int, float)


class BaseModel(object):

    DEFAULT_DAO = None

    def __init__(self, dao=None):
        if dao is None:
            dao = self.DEFAULT_DAO()
        self.dao = dao


class BreakfastModel(BaseModel):

    DEFAULT_DAO = BreakfastDao

    id = None
    name = None

    def load_by_id(self, id):
        """Load a model instance by ID"""
        dao_results = self.dao.get_by_id(id)

        if not dao_results:
            raise ValueError("No Breakfast with ID:{} found".format(id))

        self.populate(dao_results)

    def populate(self, data):
        """Populate the model properties from a map of values"""
        self.id = data.get('id', self.id)
        self.name = data.get('name', self.name)

    def to_dict(self):
        """Convert the model instance to a python dict."""
        return {
            "id": self.id,
            "name": self.name
        }


class IngredientModel(BaseModel):

    DEFAULT_DAO = IngredientDao

    id = None
    name = None

    def load_by_id(self, id):
        """Load a model instance by ID"""
        dao_results = self.dao.get_by_id(id)

        if not dao_results:
            raise ValueError("No Ingredient with ID:{} found".format(id))

        self.populate(dao_results)

    def populate(self, data):
        """Populate the model properties from a map of values"""
        self.id = data.get('id', self.id)
        self.name = data.get('name', self.name)

    def to_dict(self):
        """Convert the model instance to a python dict."""
        return {
            "id": self.id,
            "name": self.name
        }


class UserModel(BaseModel):

    DEFAULT_DAO = UserDao

    id = None
    first_name = None
    last_name = None
    preferences = None

    @property
    def full_name(self):
        """Return the user's full name by concating first and last name"""
        return " ".join((self.first_name, self.last_name))

    def load_by_id(self, id):
        """Load a user instance by the user's ID"""
        dao_results = self.dao.get_by_id(id)

        if not dao_results:
            raise ValueError("No User with ID:{} found".format(id))

        self.populate(dao_results)

    def load_by_id_with_preferences(self, id):
        """Load a user instance by the user's ID"""
        dao_results = self.dao.get_by_id_join_preferences(id)

        if not dao_results:
            raise ValueError("No UserPreference with ID:{} found".format(id))

        self.populate(dao_results)

    def populate(self, data):
        """Populate the user model properties from a map of values"""
        self.id = data.get('id', self.id)
        self.first_name = data.get('first_name', self.first_name)
        self.last_name = data.get('last_name', self.last_name)
        self.preferences = data.get('preferences')

    def to_dict(self):
        """Convert the model instance to a python dict."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

    def validate(self):
        """Validate model instance properties. Return True if all properties are valid."""

        return all([_validate_string(self.first_name),
                    _validate_string(self.last_name)])

    def save(self):
        """Save the model instance. Creates a new User if no ID is set"""
        is_success = False

        if not self.validate():
            raise ValueError('Model validation failed')

        if not self.id:
            self.id = self.dao.create(first_name=self.first_name, last_name=self.last_name)
            is_success = bool(self.id)
        else:
            is_success = self.dao.update(first_name=self.first_name, last_name=self.last_name)

        return is_success

    def delete(self):
        """Delete the model instance from the database"""
        if not self.id:
            return False
        if self.dao.delete(self.id):
            self.id = None
            return True
        else:
            return False

    def get_recommendations(self, breakfast_ingredient_dao=None):
        breakfasts = {}
        breakfast_scores = {}
        results = []

        if breakfast_ingredient_dao is None:
            breakfast_ingredient_dao = BreakfastIngredientDao()

        if self.preferences is None:
            # A future iteration could support lazy loading of preferences. For now we just raise an exception
            raise ValueError("No preferences loaded")

        if len(self.preferences) == 0:
            return []

        # Get all breakfasts and their ingredients
        for bi in breakfast_ingredient_dao.list_all():
            breakfasts.setdefault(bi['breakfast_id'], {})
            breakfasts[bi['breakfast_id']][bi['ingredient_id']] = bi['coefficient']

        # Use dot product to score similarity of breakfast ingredients and user's preferences
        for breakfast, ingredients in breakfasts.items():
            breakfast_scores[breakfast] = dot_product(ingredients, self.preferences)

        # build the results object
        for breakfast in breakfasts:
            results.append({
                'breakfast_id': breakfast,
                'score': breakfast_scores[breakfast],
            })

        # sort the results by the dot product result
        return sorted(results, reverse=True, key=lambda k: k['score'])


class UserPreferenceModel(BaseModel):

    DEFAULT_DAO = UserPreferenceDao

    id = None
    user_id = None
    ingredient_id = None
    coefficient = None

    def delete(self):
        """Delete the model instance from the database"""
        if not self.id:
            return False
        if self.dao.delete(self.id):
            self.id = None
            return True
        else:
            return False

    def load_by_id(self, id):
        """Load a user instance by the user's ID"""
        dao_results = self.dao.get_by_id(id)

        if not dao_results:
            raise ValueError("No UserPreference with ID:{} found".format(id))

        self.populate(dao_results)

    def load_by_user_ingredient(self, user_id, ingredient_id):
        dao_results = self.dao.get_by_user_ingredient(user_id, ingredient_id)

        if not dao_results:
            raise ValueError("No UserPreference for user_id:{} and ingredient_id:{} found".format(
                user_id, ingredient_id))

        self.populate(dao_results)

    def populate(self, data):
        """Populate the user model properties from a map of values"""
        self.id = data.get('id', self.id)
        self.user_id = data.get('user_id', self.user_id)
        self.ingredient_id = data.get('ingredient_id', self.ingredient_id)
        self.coefficient = data.get('coefficient', self.coefficient)

    def save(self):
        """Save the model instance. Creates a new UserPreference if no ID is set"""
        is_success = False

        if not self.validate():
            raise ValueError('Model validation failed')

        if not self.id:
            self.id = self.dao.create(user_id=self.user_id,
                                      ingredient_id=self.ingredient_id,
                                      coefficient=self.coefficient)
            is_success = bool(self.id)
        else:
            is_success = self.dao.update(id=self.id,
                                         user_id=self.user_id,
                                         ingredient_id=self.ingredient_id,
                                         coefficient=self.coefficient)

        return is_success

    def to_dict(self):
        """Convert the model instance to a python dict."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "ingredient_id": self.ingredient_id,
            "coefficient": self.coefficient
        }

    def validate(self):
        """Validate model instance properties. Return True if all properties are valid."""

        return all([_validate_int(self.user_id),
                    _validate_int(self.ingredient_id),
                    _validate_float(self.coefficient),
                    (0 <= self.coefficient <= 1)])
