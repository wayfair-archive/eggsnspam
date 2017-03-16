-- tblExample --
CREATE TABLE "tblExample" (
    id INTEGER NOT NULL, 
    name VARCHAR(100) NOT NULL, 
    PRIMARY KEY (id)
);

INSERT INTO tblExample ('id', 'name') VALUES
(1, 'Foo'),
(2, 'Bar'),
(3, 'Baz');
