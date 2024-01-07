import mysql.connector


# ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` `
# ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` `
# ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` `
# THIS FILE DELETES ALL DATA FROM DATABASES IF YOU HAVE ANYTHING BTW
# ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ 
# ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ 
# ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ 


# JUST RUN THIS FILE AND IT WILL SETUP UR DB's
























# ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` `
# ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` `
# ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` `
# CHANGE THESE LINES IN THE LIST AND RUN TO CONFIGURE YOUR LOCAL DB
# ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ 
# ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ 
# ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ 

USERS_COMMANDS = [
    "user_id VARCHAR(255) PRIMARY KEY",
    "username VARCHAR(255)",
    "password VARCHAR(255)",
    "first_name VARCHAR(255)",
    "last_name VARCHAR(255)",
    "email VARCHAR(255)",
    "phone_number VARCHAR(15)",
    "user_photo_file_name VARCHAR(255)"
]

CLOTHES_COMMANDS = [
    "clothes_id INT",
    "MODIFY COLUMN clothes_id INT AUTO_INCREMENT",
    "ADD CONSTRAINT user_id FOREIGN KEY (user_id) REFERENCES Users(user_id);",
    "clothing_type VARCHAR(255)",
    "is_clean TINYINT(1)",
    "hue INT",
    "saturation INT",
    "value INT",
    "tone VARCHAR(255)",
    "colortemp VARCHAR(255)",
    "clothing_name VARCHAR(255)",
    "clothingimg_filepath VARCHAR(255)"
]

# ONLY CHANGE THESE IF WE ADD MORE DB's

TABLES = {
    "Users" : USERS_COMMANDS,
    "Clothes" : CLOTHES_COMMANDS
}

password = input("MYSQL Password: ")
password = password.strip()
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password
)

cursor = connection.cursor()

def delete_table(table_name):
    cursor.execute(f"DROP TABLE {table_name}")

def create_databases():
    #cursor.execute("CREATE DATABASE Poshify")
    cursor.execute(f"USE Poshify")
    try:
        cursor.execute(f"DROP TABLE Clothes")
    except:
        print("No table to drop: Clothes.")
    try:
        cursor.execute(f"DROP TABLE Users")
    except:
        print("No table to drop: Users.")
    try:
        cursor.execute(f"DROP TABLE Calendar")
    except:
        print("No table to drop: Calendar.")

    cursor.execute(f"""
        CREATE TABLE Users (
            user_id VARCHAR(255),
            PRIMARY KEY (user_id),
            username VARCHAR(255),
            password VARCHAR(255),
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            email VARCHAR(255),
            phone_number VARCHAR(15),
            user_photo_file_name VARCHAR(255)
        );
    """)

    cursor.execute(f"""
        CREATE TABLE Clothes (
            clothes_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255),
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            clothing_type VARCHAR(255),
            clothing_name VARCHAR(255),
            is_clean TINYINT(1),
            hue INT,
            saturation INT,
            value INT,
            tone VARCHAR(255),
            colortemp VARCHAR(255),
            clothingimg_filepath VARCHAR(255)
        );
    """)
    cursor.execute(f"""
        CREATE TABLE Calendar (
            outfit_id INT AUTO_INCREMENT PRIMARY KEY,
            user_id VARCHAR(255),
            FOREIGN KEY (user_id) REFERENCES Users(user_id),
            clothes_id INT,
            FOREIGN KEY (clothes_id) REFERENCES Clothes(clothes_id),
            dayOfWeek VARCHAR(255),
            filepath VARCHAR(255),
            outfitType VARCHAR(255),
            date VARCHAR(6)
        );
    """)

    print("Created DB's")


def init_database():
    try:
        cursor.execute(f"USE Poshify")
        print(f"Sucess: Accessed 'Poshify'")
    except mysql.connector.Error as err:
        cursor.execute(f"CREATE DATABASE Poshify")
        cursor.execute(f"USE Poshify")
        print(f"Sucess: Creating 'Poshify'")

def init_table(table_name):
    try:
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        if cursor.fetchone() is None:
            cursor.execute(f"CREATE TABLE {table_name};")
            cursor.execute(f"ALTER TABLE {table_name};")
            print(f"Creating '{table_name}': Success")
        else:
            print(f"Success: Accessing '{table_name}'")
    except Exception as e:
        print(f"Error: init_table {e}")

def init_column(table_name, command):
    try:
        cursor.execute(f"ALTER TABLE {table_name} MODIFY COLUMN {command};")
        print(f"Success: Changed data type of column '{command.split()[1]} in {table_name}")
    except mysql.connector.Error as err:
        try:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {command};")
            print(f"Success: Added {command} to {table_name}.")
        except mysql.connector.Error as err:
            print(f"Failure: Cannot add or modify column {command} to {table_name}.")

def create_database():

    create_databases()

    # init_database()
    # for table_name in TABLES:
    #     init_table(table_name)
    #     for command in TABLES[table_name]:
    #         init_column(table_name, command)

if __name__ == "__main__":
    create_database()

connection.commit()
cursor.close()
connection.close()