"""SQLAlchemy model definitions."""

from eggsnspam.common.recommendations import dot_product
from eggsnspam.extensions import db


class Breakfast(db.Model):
    """Defines the breakfast table."""

    __tablename__ = 'tblBreakfast'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('Name', db.String(100), nullable=False)

    ingredients = db.relationship(
        'BreakfastIngredient',
        backref='breakfast'
    )

    def __unicode__(self):
        """The string representation of the object instance."""
        return u'<Breakfast %s>' % self.name

    def to_dict(self):
        """Convert the object instance to a python dict."""
        return {k: v for k, v in self.__dict__.items() if k != "_sa_instance_state"}


class Ingredient(db.Model):
    """Defines the ingredient table."""

    __tablename__ = 'tblIngredient'

    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), nullable=False)

    preferences = db.relationship(
        'UserPreference',
        backref='ingredient'
    )

    breakfast_ingredients = db.relationship(
        'BreakfastIngredient',
        backref='ingredient'
    )

    def to_dict(self):
        """Convert the object instance to a python dict."""
        return {k: v for k, v in self.__dict__.items() if k != "_sa_instance_state"}


class User(db.Model):
    """Defines the user table."""

    __tablename__ = 'tblUser'

    id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(100), nullable=False)
    last_name = db.Column('last_name', db.String(100), nullable=False)

    preferences = db.relationship(
        'UserPreference',
        backref='user'
    )

    @property
    def full_name(self):
        return u"{} {}".format(self.first_name, self.last_name)

    def __unicode__(self):
        """The string representation of the object instance."""
        return u'<User %s>' % self.full_name

    def to_dict(self):
        """Convert the object instance to a python dict."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name
        }

    def get_recommendations(self):
        """Get breakfast recommendations using dot_product"""
        breakfasts = {}
        breakfast_scores = {}
        results = []

        # Get all the user's ingredient preferences
        user_prefs = {p.ingredient_id: p.coefficient for p in self.preferences}

        # Get all breakfasts and their ingredients
        for bi in BreakfastIngredient.query.with_hint(BreakfastIngredient, "WITH (NOLOCK)").all():
            breakfasts.setdefault(bi.breakfast_id, {})
            breakfasts[bi.breakfast_id][bi.ingredient_id] = bi.coefficient

        # Use dot product to score similarity of breakfast ingredients and user's preferences
        for breakfast, ingredients in breakfasts.items():
            breakfast_scores[breakfast] = dot_product(ingredients, user_prefs)

        # build the results object
        for breakfast in breakfasts:
            results.append({
                'breakfast_id': breakfast,
                'score': breakfast_scores[breakfast],
            })

        # sort the results by the dot product result
        return sorted(results, reverse=True, key=lambda k: k['score'])


class BreakfastIngredient(db.Model):

    __tablename__ = 'tblBreakfastIngredient'

    breakfast_id = db.Column(db.Integer, db.ForeignKey('tblBreakfast.id'), primary_key=True)
    ingredient_id = db.Column('ingredient_id', db.Integer, db.ForeignKey('tblIngredient.id'), primary_key=True)
    coefficient = db.Column('coefficient', db.Float, nullable=False)

    def to_dict(self):
        """Convert the object instance to a python dict."""
        return {
            'breakfast_id': self.breakfast_id,
            'ingredient_id': self.ingredient_id,
            'coefficient': self.coefficient
        }


class UserPreference(db.Model):

    __tablename__ = 'tblUserPreferences'

    user_id = db.Column(db.Integer, db.ForeignKey('tblUser.id'), primary_key=True)
    ingredient_id = db.Column('ingredient_id', db.Integer, db.ForeignKey('tblIngredient.id'), primary_key=True)
    coefficient = db.Column('coefficient', db.Float, nullable=False)

    def to_dict(self):
        """Convert the object instance to a python dict."""
        return {
            'user_id': self.user_id,
            'ingredient_id': self.ingredient_id,
            'coefficient': self.coefficient
        }
