
CREATE TABLE genres(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password TEXT,
    admin BOOLEAN
);
CREATE TABLE movies (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    description TEXT,
    genreid INT REFERENCES genres,
    cover BYTEA
);

CREATE TABLE reviews(
    id SERIAL PRIMARY KEY,
    description TEXT,
    stars INT,
    date DATE,
    userid INT REFERENCES users,
    movieid INT REFERENCES movies
);

CREATE TABLE requests (
    userid INT REFERENCES users,
    movieid INT REFERENCES movies
);

INSERT INTO genres (name) VALUES
('Comedy'),
('Horror'),
('Documentary'),
('Sci-Fi'),
('Fantasy'),
('Drama'),
('Romance'),
('Thriller'),
('Mystery'),
('Action'),
('Adventure'),
('Educational'),
('Commercial'),
('Musical');