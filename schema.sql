CREATE TABLE authors 
	(id SERIAL PRIMARY KEY, 
	name TEXT);
CREATE TABLE genres 
	(id SERIAL PRIMARY KEY, 
	name TEXT);
CREATE TABLE books 
	(id SERIAL PRIMARY KEY, 
	name TEXT, 
	author_id INTEGER REFERENCES authors,
	genre_id INTEGER REFERENCES genres);
CREATE TABLE reviews 
	(id SERIAL PRIMARY KEY, 
	stars NUMERIC,
	book_id INTEGER REFERENCES books);
CREATE TABLE users 
	(id SERIAL PRIMARY KEY, 
	username TEXT,
	password TEXT,
	admin BOOLEAN);



