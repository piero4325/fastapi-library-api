create table authors(
	id SERIAL PRIMARY key,
	name VARCHAR(100) NOT NULL,
	country VARCHAR(50)
);

INSERT INTO authors (name, country) VALUES
('Fyodor Dostoevsky', 'Russia'),
('Leo Tolstoy', 'Russia'),
('George Orwell', 'United Kingdom'),
('Gabriel Garcia Marquez', 'Colombia'),
('Haruki Murakami', 'Japan');



CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    year INTEGER,
    author_id INTEGER NOT NULL,
    FOREIGN KEY (author_id) REFERENCES authors(id)
);


INSERT INTO books (title, year, author_id) VALUES
('Crime and Punishment', 1866, 1),
('The Brothers Karamazov', 1880, 1),
('War and Peace', 1869, 2),
('Anna Karenina', 1877, 2),
('1984', 1949, 3),
('Animal Farm', 1945, 3),
('One Hundred Years of Solitude', 1967, 4),
('Norwegian Wood', 1987, 5);

