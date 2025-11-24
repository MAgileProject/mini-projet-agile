
CREATE DATABASE IF NOT EXISTS adoption_animals;
USE adoption_animals;

CREATE TABLE person (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    
    -- Pour représenter l’héritage User/Admin
    role ENUM('user', 'admin') NOT NULL
);

CREATE TABLE animal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    description TEXT,
    image VARCHAR(255)
);


CREATE TABLE publication_request (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    animalInfo TEXT NOT NULL,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_pub_user 
        FOREIGN KEY (user_id) REFERENCES person(id)
        ON DELETE CASCADE
);


CREATE TABLE adoption_request (
    id INT AUTO_INCREMENT PRIMARY KEY,
    animal_id INT NOT NULL,
    user_id INT NOT NULL,
    date_request DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    appointment_date DATETIME,
    
    CONSTRAINT fk_adopt_animal
        FOREIGN KEY (animal_id) REFERENCES animal(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_adopt_user
        FOREIGN KEY (user_id) REFERENCES person(id)
        ON DELETE CASCADE
);
