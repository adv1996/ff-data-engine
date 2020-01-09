-- SQLite
DROP TABLE users;
CREATE TABLE users (
    user_id CHAR(50) PRIMARY KEY,
    username CHAR(25) NOT NULL
);