DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS purchase;

CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    author TEXT,
    year INTEGER,
    edition TEXT,
    publisher TEXT,
    condition TEXT,
    description TEXT,
    price INTEGER,
    sellerID INTEGER,
    FOREIGN KEY (sellerID) REFERENCES user (id)
);

CREATE TABLE purchase (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    bookID INTEGER,
    date TEXT,
    buyerID INTEGER,
    FOREIGN KEY (buyerID) REFERENCES user (id),
    FOREIGN KEY (bookID) REFERENCES book (id)
);
