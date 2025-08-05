CREATE TABLE authors(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE
);

CREATE TABLE books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    price TEXT,
    stock TEXT,
    rating TEXT,
    upc TEXT UNIQUE,
    url TEXT
);

CREATE TABLE book_authors(
    book_id INTEGER,
    author_id INTEGER,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (author_id) REFERENCES authors(id)
);