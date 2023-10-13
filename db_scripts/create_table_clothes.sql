CREATE TABLE Clothes (
    clothes_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    clothing_type VARCHAR(255),
    is_clean BOOLEAN
);