from sqlalchemy.sql.expression import text

from eggsnspam.common.daos import SqlBaseDao

from ..extensions import db


class BreakfastDao(SqlBaseDao):

    def get_by_id(self, id):
        """Retrieve a record from the database by ID"""
        query = text("""
        SELECT id, name FROM tblBreakfast
        WHERE id=:id;
        """)
        return self.fetchone(query, id=id)

    def list_all(self):
        """Get all records from the database"""
        query = text("""
        SELECT id, name FROM tblBreakfast;
        """)
        return self.fetchall(query)


class IngredientDao(SqlBaseDao):

    def get_by_id(self, id):
        """Retrieve a record from the database by ID"""
        query = text("""
        SELECT id, name FROM tblIngredient
        WHERE id=:id;
        """)
        return self.fetchone(query, id=id)

    def list_all(self):
        """Get all records from the database"""
        query = text("""
        SELECT id, name FROM tblIngredient;
        """)
        return self.fetchall(query)


class UserDao(SqlBaseDao):

    def get_by_id(self, id):
        """Retrieve a record from the database by ID"""
        query = text("""
        SELECT id, first_name, last_name FROM tblUser
        WHERE id=:id;
        """)
        return self.fetchone(query, id=id)

    def get_by_id_join_preferences(self, id):
        """Retrieve a record from the database by ID"""
        query = text("""
        SELECT
            tblUser.id as id,
            tblUser.first_name as first_name,
            tblUser.last_name as last_name,
            tblUserPreference.ingredient_id as ingredient_id,
            tblUserPreference.coefficient as coefficient
        FROM tblUser
        LEFT OUTER JOIN tblUserPreference ON tblUser.id = tblUserPreference.user_id
        WHERE tblUser.id=:id;
        """)
        result = self.fetchall(query, id=id)

        if len(result) == 0:
            return None

        preferences = {}
        for r in filter(lambda x: x['ingredient_id'] is not None, result):
            preferences[r['ingredient_id']] = r['coefficient']

        return {
            'id': result[0]['id'],
            'first_name': result[0]['first_name'],
            'last_name': result[0]['last_name'],
            'preferences': preferences
        }

    def create(self, first_name, last_name):
        """Create a new record in the database"""
        query = text("""
        INSERT INTO tblUser
            (first_name, last_name)
        VALUES
            (:first_name, :last_name);
        """)
        result = self.execute(query, first_name=first_name, last_name=last_name)
        db.session.commit()
        return result.lastrowid

    def update(self, id, first_name, last_name):
        """Update a record in the database with new values"""
        query = text("""
        UPDATE tblUser SET
            first_name=:first_name,
            last_name=:last_name
        WHERE
            id=:id
        """)
        result = self.execute(query,
                              id=id,
                              first_name=first_name,
                              last_name=last_name)
        db.session.commit()
        return result.rowcount > 0

    def delete(self, id):
        """Delete a record from the database for an ID"""
        query = text("""
        DELETE FROM tblUser WHERE id=:id
        """)
        result = self.execute(query, id=id)
        return result.rowcount > 0

    def list_all(self):
        """Get all records from the database"""
        query = text("""
        SELECT id, first_name, last_name FROM tblUser;
        """)
        return self.fetchall(query)


class UserPreferenceDao(SqlBaseDao):

    def get_by_id(self, id):
        """Retrieve a record from the database by ID"""
        query = text("""
        SELECT id, user_id, ingredient_id, coefficient FROM tblUserPreference
        WHERE id=:id;
        """)
        return self.fetchone(query, id=id)

    def get_by_user_ingredient(self, user_id, ingredient_id):
        """Retrieve a record from the database by ID"""
        query = text("""
        SELECT id, user_id, ingredient_id, coefficient FROM tblUserPreference
        WHERE user_id=:user_id AND ingredient_id=:ingredient_id;
        """)
        return self.fetchone(query, user_id=user_id, ingredient_id=ingredient_id)

    def create(self, user_id, ingredient_id, coefficient):
        """Create a new record in the database"""
        query = text("""
        INSERT INTO tblUserPreference
            (user_id, ingredient_id, coefficient)
        VALUES
            (:user_id, :ingredient_id, :coefficient);
        """)
        result = self.execute(query,
                              user_id=user_id,
                              ingredient_id=ingredient_id,
                              coefficient=coefficient)
        db.session.commit()
        return result.lastrowid

    def update(self, id, user_id, ingredient_id, coefficient):
        """Update a record in the database with new values"""
        query = text("""
        UPDATE tblUserPreference SET
            user_id=:user_id,
            ingredient_id=:ingredient_id,
            coefficient=:coefficient
        WHERE
            id=:id
        """)
        result = self.execute(query,
                              id=id,
                              user_id=user_id,
                              ingredient_id=ingredient_id,
                              coefficient=coefficient)
        db.session.commit()
        return result.rowcount > 0

    def delete(self, id):
        """Delete a record from the database for an ID"""
        query = text("""
        DELETE FROM tblUserPreference WHERE id=:id
        """)
        result = self.execute(query, id=id)
        return result.rowcount > 0

    def list_all_for_user(self, user_id):
        """Get all records from the database"""
        query = text("""
        SELECT id, user_id, ingredient_id, coefficient FROM tblUserPreference
        WHERE user_id=:user_id;
        """)
        return self.fetchall(query, user_id=user_id)


class BreakfastIngredientDao(SqlBaseDao):

    def list_all(self):
        """Get all ingredients for all breakfasts"""

        query = text("""
        SELECT breakfast_id, ingredient_id, coefficient FROM tblBreakfastIngredient;
        """)

        return self.fetchall(query)
