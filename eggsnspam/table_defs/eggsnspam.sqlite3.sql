CREATE TABLE IF NOT EXISTS "tblBreakfast" (
    "id" INTEGER NOT NULL, 
    "name" VARCHAR(100) NOT NULL, 
    PRIMARY KEY ("ID")
);


CREATE TABLE IF NOT EXISTS "tblIngredient" (
    "id" INTEGER NOT NULL, 
    "name" VARCHAR(100) NOT NULL, 
    PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS "tblUser" (
    "id" INTEGER NOT NULL, 
    "first_name" VARCHAR(100) NOT NULL, 
    "last_name" VARCHAR(100) NOT NULL, 
    PRIMARY KEY ("ID")
);

CREATE TABLE IF NOT EXISTS 'tblBreakfastIngredient' (
    id INTEGER NOT NULL, 
    breakfast_id INTEGER, 
    ingredient_id INTEGER, 
    coefficient FLOAT, 
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS 'tblUserPreference' (
    id INTEGER NOT NULL, 
    user_id INTEGER, 
    ingredient_id INTEGER, 
    coefficient FLOAT, 
    PRIMARY KEY (id)
);
