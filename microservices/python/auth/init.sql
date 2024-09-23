-- Drop database
DROP DATABASE IF EXISTS auth;

-- Create database + user if doesn't exist
CREATE DATABASE IF NOT EXISTS auth;
CREATE USER IF NOT EXISTS 'auth_user'@'localhost';
SET PASSWORD FOR 'auth_user'@'localhost' = 'Auth123';
GRANT ALL ON auth.* TO 'auth_user'@'localhost';
GRANT SELECT ON performance_schema.* TO 'auth_user'@'localhost';
FLUSH PRIVILEGES;

USE auth;

DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (`id`)
);

LOCK TABLES `user` WRITE;

INSERT INTO user (email, password) VALUES ("example@email.com", "password123");

UNLOCK TABLES;
