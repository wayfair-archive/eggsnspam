import factory

from eggsnspam.oop_orm import models


class BreakfastFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = models.Breakfast

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: "breakfast-{}".format(n))


class IngredientFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = models.Ingredient

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: "ingredient-{}".format(n))


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = models.User

    id = factory.Sequence(lambda n: n)
    first_name = factory.Sequence(lambda n: "User-{}".format(n))
    last_name = "McTester"


class UserPreferenceFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = models.UserPreference

    user = factory.SubFactory(UserFactory)
    ingredient = factory.SubFactory(IngredientFactory)
    coefficient = 0.5


class BreakfastIngredientFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = models.BreakfastIngredient

    breakfast = factory.SubFactory(BreakfastFactory)
    ingredient = factory.SubFactory(IngredientFactory)
    coefficient = 0.5
