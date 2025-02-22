create database pune;
use pune;

CREATE TABLE students (
    prn VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE cards (
    id VARCHAR(10),  -- PRN if student, NULL otherwise
    name VARCHAR(100) NOT NULL,
    cardno INT(6) UNIQUE NOT NULL,
    balance DECIMAL(10,2) DEFAULT 0,
    PRIMARY KEY (cardno),
    FOREIGN KEY (id) REFERENCES students(prn) ON DELETE SET NULL
);

CREATE TABLE stations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cardno INT(6) NOT NULL,
    type ENUM('Top-up', 'Fare') NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cardno) REFERENCES cards(cardno) ON DELETE CASCADE
);

CREATE TABLE rides (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cardno INT(6) NOT NULL,
    source_station INT NOT NULL,
    destination_station INT NOT NULL,
    fare DECIMAL(10,2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cardno) REFERENCES cards(cardno) ON DELETE CASCADE,
    FOREIGN KEY (source_station) REFERENCES stations(id) ON DELETE CASCADE,
    FOREIGN KEY (destination_station) REFERENCES stations(id) ON DELETE CASCADE
);
