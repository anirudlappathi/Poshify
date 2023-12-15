CREATE TABLE Clothes (
    clothes_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    clothing_name VARCHAR(255),
    clothing_type VARCHAR(255),
    color VARCHAR(255),
    is_clean BOOLEAN
    hue INT
    saturation INT
    value INT
    tone INT
    colortemp INT
);

-- mysql -u root -p
-- [ENTER PASSWORD]
-- USE Poshify;
-- ALTER TABLE Clothes
-- ADD COLUMN color VARCHAR(255);
-- 