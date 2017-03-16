from sqlalchemy.sql.expression import text

from eggsnspam.common.daos import SqlBaseDao


class BreakfastRecsDao(SqlBaseDao):

    def get_ingredient_preferences(self, user_id):
        """Get a person's prefernces for each breakfast attribute"""

        query = text("""
        SELECT ingredient_id, coefficient FROM tblUserPreference
        WHERE user_id=:user_id;
        """)

        return self.fetchmany(query, user_id=user_id)

    def get_all_breakfast_ingredients(self):
        """Get all ingredients for all breakfasts"""

        query = text("""
        SELECT breakfast_id, ingredient_id, coefficient FROM tblBreakfastIngredient;
        """)

        return self.fetchall(query)
