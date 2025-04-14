create database PuneMetro;
use PuneMetro;

CREATE TABLE students (
    prn VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

create table admin(
    adminID int primary key,
    name varchar(50) not null,
    email varchar(50),
    password varchar(20)
);

CREATE TABLE users (
    userID INT UNIQUE AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(50) PRIMARY KEY,
    usertype VARCHAR(20) NOT NULL
);

ALTER TABLE users AUTO_INCREMENT = 101;

CREATE TABLE ctype (
    cardtype VARCHAR(25) PRIMARY KEY,
    discount_in_percent INT DEFAULT 0 CHECK (discount_in_percent >= 0 AND discount_in_percent <= 100)
);

CREATE TABLE cards (
    cardID INT PRIMARY KEY AUTO_INCREMENT,
    userID INT NOT NULL,
    cardtype VARCHAR(25) NOT NULL,
    balance DECIMAL(10, 2) NOT NULL CHECK (balance >= 0),
    issuedate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userID) REFERENCES users(userID) ON DELETE CASCADE,
    FOREIGN KEY (cardtype) REFERENCES ctype(cardtype) ON DELETE CASCADE
);

CREATE TABLE stations (
    stationID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

ALTER TABLE stations AUTO_INCREMENT = 1;

CREATE TABLE transactions (
    transID INT AUTO_INCREMENT PRIMARY KEY,
    cardID INT default null,
    departID INT NOT NULL,
    arrivalID INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    timed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cardID) REFERENCES cards(cardID) on delete CASCADE,
    FOREIGN KEY (departID) REFERENCES stations(stationID) on delete CASCADE,
    FOREIGN KEY (arrivalID) REFERENCES stations(stationID) on delete CASCADE
);
