import psycopg2
import os
import traceback
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}


class FishDatabase:
    @staticmethod
    def connect():
        try:
            connection = psycopg2.connect(**DB_CONFIG)
            return connection
        except Exception:
            print("Error ocurred in making connection.")
            traceback.print_exc()  # Print the whole exception log

    @staticmethod
    def register_user(connection, user_id, username):
        """
        Register a new user in the database

        Args:
            user_id (str): Discord user ID
            username (str): Discord username

        Returns:
            tuple: (success (bool), message (str))
        """
        cursor = connection.cursor()

        if not connection:
            return False, "Failed to connect to database"

        try:
            cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
            if cursor.fetchone():
                cursor.close()
                connection.close()
                return False, "User already registered"

            # Reset time is set to next dat at midnight UTC
            tomorrow = datetime.now() + timedelta(days=1)
            reset_time = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)

            # Insert new user
            query = """
            INSERT INTO users (user_idm username, fishing_attempts_left, fishing_attempts_reset_at)
            VALUES (%s, %s, 5, %s)
            """
            cursor.execute(query, (user_id, username, reset_time))
            connection.commit()

            # Create initial habit streak entry
            # We'll setup the habit system later, but this initializes necessary data
            cursor.close()
            connection.close()
            return True, "User registered successfully!"

        except Exception as err:
            cursor.close()
            connection.rollback()
            connection.close()
            print(f"Error registering user: {err}")
            traceback.print_exc()
            return False, "Error registering user"

    @staticmethod
    def get_user(connection, user_id):
        """
        Get user data from database

        Args:
            user_id (str): Discord user ID

        Returns:
            dict or None: User data or None if user not found
        """
        if not connection:
            return None

        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT user_id, username, fishing_attempts_left, fishing_attempts_reset_at, current_rod_id"
                "FROM users WHERE user_id = %s",
                (user_id,),
            )
            user_data = cursor.fetchone()

            if not user_data:
                cursor.close()
                connection.close()
                return None

            # Convert to dict for easier access
            user = {
                "user_ud": user_data[0],
                "username": user_data[1],
                "fishing_attempts_left": user_data[2],
                "fishing_attempts_reset_at": user_data[3],
                "current_rod_id": user_data[4],
            }

            cursor.close()
            connection.close()
            return user

        except Exception as err:
            cursor.close()
            connection.close()
            print(f"Error getting user: {err}")
            traceback.print_exc()
            return None

    @staticmethod
    def check_reset_fishing_attempts(connection, user_id):
        """ "
        Check if fishing attempts should be reset and reset them if needed

        Args:
            user_id (str): Discord user ID

        Returns:
            bool: True if reset was performed, False otherwise
        """
        if not connection:
            return False

        cursor = connection.cursor()
        try:
            # Check if reset time has passed
            cursor.execute(
                "SELECT fishing_attempts_reset_at FROM users WHERE user_id = %s",
                (user_id,),
            )
            result = cursor.fetchone()

            if not result:
                cursor.close()
                connection.close()
                return False

            reset_time = result[0]
            now = datetime.now()

            # If current time is past reset time, reset attempts
            if now >= reset_time:
                # Calculate next reset time (next day at midnight UTC)
                tomorrow = now + timedelta(days=1)
                next_reset = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)

                # Reset attempts
                cursor.execute(
                    "UPDATE users SET fishing_attempts_left = 5, fishing_attempts_reset_at = %s "
                    "WHERE user_id = %s",
                    (next_reset, user_id),
                )
                connection.commit()
                cursor.close()
                connection.close()
                return True

            cursor.close()
            connection.close()
            return False

        except Exception as err:
            cursor.close()
            connection.rollback()
            connection.close()
            print(f"Error checking/resetting fishing attempts: {err}")
            traceback.print_exc()
            return False

    @staticmethod
    def insert_fish(connection, name: str, rarity: str, catch_rate: float):
        cursor = connection.cursor()
        # Insert fish if it's not in the table already
        query = """
        INSERT INTO fish_types (name, rarity, base_catch_rate)
        VALUES (%s, %s, %s)
        ON CONFLICT (name)
        DO NOTHING;
        """

        try:
            data = (name, rarity, catch_rate)
            cursor.execute(query, data)
            connection.commit()
            print("Record inserted successfully!")
        except Exception as err:
            print(err)

        cursor.close()
        connection.close()

    @staticmethod
    def sample_fish_from_rarity(connection, rarity: str):
        cursor = connection.cursor()
        try:
            # Get a random fish of the chosen rarity
            cursor.execute(
                "SELECT name FROM fish_types WHERE rarity = %s ORDER BY RANDOM() LIMIT 1",
                (rarity,),
            )
            record = cursor.fetchone()
            fish = record[0]
            print(f"Read successful. name = {fish}")
            connection.commit()
        except Exception as err:
            print(err)
            fish = None

        cursor.close()
        connection.close()
        return fish

    @staticmethod
    def get_fish_catch_rate(connection, name: str):
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT base_catch_rate FROM fish_types WHERE name = %s",
                (name,),
            )
            record = cursor.fetchone()
            catch_rate = record[0]
            print(f"Read successful. catch_rate = {catch_rate}")
            connection.commit()
        except Exception as err:
            print(err)
            catch_rate = None

        cursor.close()
        connection.close()

        return catch_rate
