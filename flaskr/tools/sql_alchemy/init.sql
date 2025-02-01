-- Create Authors Table
CREATE TABLE authors (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

-- Create Books Table
CREATE TABLE books (
    id INTEGER PRIMARY KEY,
	 title VARCHAR(100) NOT NULL,
    author_id INTEGER,
    FOREIGN KEY (author_id) REFERENCES authors(id)
);

-- Insert Author Data
INSERT INTO authors (id, name) VALUES (1, 'F. Scott Fitzgerald');
INSERT INTO authors (id, name) VALUES (2, 'George Orwell');
INSERT INTO authors (id, name) VALUES (3, 'Jane Austen');

-- Insert Book Data
INSERT INTO books (id, title, author_id) VALUES (1, 'The Great Gatsby', 1);
INSERT INTO books (id, title, author_id) VALUES (2, '1984', 2);
INSERT INTO books (id, title, author_id) VALUES (3, 'Pride and Prejudice', 3);
