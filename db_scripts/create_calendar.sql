CREATE TABLE Calendar (
    outfit_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    clothes_id INT,
    FOREIGN KEY (clothes_id) REFERENCES Clothes(clothes_id),
    dayOfWeek VARCHAR(255),
    filepath VARCHAR(255),
    outfitType VARCHAR(255)
);

-- mysql -u root -p
-- [ENTER PASSWORD]
-- USE Poshify;
-- ALTER TABLE Clothes
-- ADD COLUMN color VARCHAR(255);
-- 