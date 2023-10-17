import unittest
import mysql.connector
import getpass
import users_db

cursor, conn = users_db.create_connection()

class TestUserFunctions(unittest.TestCase):

    global cursor
    global conn

    def setUp(self):
        # Set up any prerequisites needed for your tests
        # For example, you might want to create a test user before running tests
        pass

    def tearDown(self):
        # Clean up after the tests
        pass

    def test_create_user(self):
        # Test creating a new user
        users_db.create_user("1", "test_user", "Test", "User", "test@example.com", "1234567890", "test_user.jpg")
        # Add assertions to check if the user was created successfully

    def test_get_all_users(self):
        # Test retrieving all users
        users_db.users = users_db.get_all_users(cursor, conn)
        # Add assertions to check if the expected data is returned

    def test_get_user_by_id(self):
        # Test retrieving a user by ID
        user_id = 1  # Replace with an actual user ID from your database
        users_db.user = users_db.get_user_by_id(user_id)
        # Add assertions to check if the expected data is returned

    def test_update_user(self):
        # Test updating user information
        user_id = 1  # Replace with an actual user ID from your database
        users_db.update_user(user_id, "new_username", "New", "User", "new@example.com", "9876543210", "new_user.jpg")
        # Add assertions to check if the user was updated successfully

    def test_delete_user(self):
        # Test deleting a user
        user_id = 2  # Replace with an actual user ID from your database
        users_db.delete_user(user_id)
        # Add assertions to check if the user was deleted successfully


if __name__ == '__main__':
    unittest.main()
    users_db.close_connection(cursor, conn)
