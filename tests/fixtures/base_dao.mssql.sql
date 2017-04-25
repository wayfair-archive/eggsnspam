IF NOT EXISTS (SELECT * FROM sysobjects WHERE id = object_id(N'[dbo].[tblExample]'))
CREATE TABLE [dbo].[tblExample] (
    id INTEGER IDENTITY(1, 1),
    name VARCHAR(100) NOT NULL, 
);

SET IDENTITY_INSERT tblExample ON;
DELETE FROM tblExample;
INSERT INTO tblExample (id, name) VALUES
(1, 'Foo'),
(2, 'Bar'),
(3, 'Baz');
SET IDENTITY_INSERT tblExample OFF;
