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
	genre_id INTEGER REFERENCES genres,
	publisher TEXT,
	published_in TEXT,
	year NUMERIC,
	isbn TEXT);
CREATE TABLE reviews 
	(id SERIAL PRIMARY KEY, 
	stars NUMERIC,
	book_id INTEGER REFERENCES books,
	user_id INTEGER REFERENCES users);
CREATE TABLE users 
	(id SERIAL PRIMARY KEY, 
	username TEXT,
	password TEXT,
	admin BOOLEAN);
CREATE TABLE lists
	(user_id INTEGER REFERENCES users,
	book_id INTEGER REFERENCES books);



