SET IDENTITY_INSERT tblBreakfast ON;
DELETE FROM tblBreakfast;
INSERT INTO tblBreakfast (id, name) VALUES
(1, 'Eggs and Spam'),
(2, 'Pancakes'),
(3, 'Fruit');
SET IDENTITY_INSERT tblBreakfast OFF;

SET IDENTITY_INSERT tblIngredient ON;
DELETE FROM tblIngredient;
INSERT INTO tblIngredient (id, name) VALUES
(1, 'Eggs'),
(2, 'Spam'),
(3, 'Cantelope');
SET IDENTITY_INSERT tblIngredient OFF;

SET IDENTITY_INSERT tblUser ON;
DELETE FROM tblUser;
INSERT INTO tblUser (id, first_name, last_name) VALUES
(1, 'Adam', 'Anderson'),
(2, 'Betty', 'Blevins'),
(3, 'Carl', 'Cadigan'),
(4, 'Donnie', 'Darko');
SET IDENTITY_INSERT tblUser OFF;

DELETE FROM tblBreakfastIngredient;
INSERT INTO tblBreakfastIngredient (breakfast_id, ingredient_id, coefficient) VALUES
(1, 1, 0.8),
(1, 2, 0.8),
(1, 3, 0.2),
(2, 1, 0.0),
(2, 2, 0.2),
(2, 3, 0.9),
(3, 1, 0.9),
(3, 2, 0.5),
(3, 3, 0.1);

DELETE FROM tblUserPreference;
INSERT INTO tblUserPreference (user_id, ingredient_id, coefficient) VALUES
(1, 1, 0.8),
(1, 2, 0.4),
(1, 3, 0.6),
(2, 1, 0.9),
(2, 2, 0.3),
(2, 3, 0.1),
(3, 1, 0.8),
(3, 2, 0.9),
(3, 3, 0.8);
