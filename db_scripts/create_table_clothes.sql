CREATE TABLE Clothes (
    clothes_id AUTO_INCREMENT INT,
    MODIFY COLUMN clothes_id INT AUTO_INCREMENT,
    ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES Users(user_id);,
    clothing_type VARCHAR(255),
    is_clean TINYINT(1),
    color VARCHAR(255),
    hue INT,
    saturation INT,
    value INT,
    tone VARCHAR(255),
    colortemp VARCHAR(255),
    clothing_name VARCHAR(255),
    until_dirty INT,
    worn_count INT,
);

-- mysql -u root -p
-- [ENTER PASSWORD]
-- USE Poshify;
-- ALTER TABLE Clothes
-- ADD COLUMN color VARCHAR(255);
-- 