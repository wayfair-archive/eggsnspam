IF NOT EXISTS (SELECT * FROM sysobjects WHERE id = object_id(N'[dbo].[tblBreakfast]'))
CREATE TABLE [dbo].[tblBreakfast] (
    id INTEGER IDENTITY(1, 1),
    name VARCHAR(100) NOT NULL, 
);

IF NOT EXISTS (SELECT * FROM sysobjects WHERE id = object_id(N'[dbo].[tblIngredient]'))
CREATE TABLE [dbo].[tblIngredient] (
    id INTEGER IDENTITY(1, 1),
    name VARCHAR(100) NOT NULL, 
);

IF NOT EXISTS (SELECT * FROM sysobjects WHERE id = object_id(N'[dbo].[tblUser]'))
CREATE TABLE [dbo].[tblUser] (
    id INTEGER IDENTITY(1, 1),
    first_name VARCHAR(100) NOT NULL, 
    last_name VARCHAR(100) NOT NULL, 
);

IF NOT EXISTS (SELECT * FROM sysobjects WHERE id = object_id(N'[dbo].[tblBreakfastIngredient]'))
CREATE TABLE [dbo].[tblBreakfastIngredient] (
    id INTEGER IDENTITY(1, 1),
    breakfast_id INTEGER, 
    ingredient_id INTEGER, 
    coefficient FLOAT, 
);

IF NOT EXISTS (SELECT * FROM sysobjects WHERE id = object_id(N'[dbo].[tblUserPreference]'))
CREATE TABLE [dbo].[tblUserPreference] (
    id INTEGER IDENTITY(1, 1),
    user_id INTEGER, 
    ingredient_id INTEGER, 
    coefficient FLOAT, 
);
