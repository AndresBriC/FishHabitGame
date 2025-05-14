import psycopg2
from psycopg2.extras import execute_values
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
            INSERT INTO users (user_id, username, fishing_attempts_left, fishing_attempts_reset_at)
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
                """SELECT user_id, username, fishing_attempts_left, fishing_attempts_reset_at, pond_size, current_rod_id
                FROM users WHERE user_id = %s""",
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
                "pond_size": user_data[4],
                "current_rod_id": user_data[5],
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
    def see_user_pond(connection, user_id):
        """
        Gets the fish id and names for a specific user in their pond.

        Args:
            connection: psycopg2 connection object
            user_id (str): Discord user ID

        Returns:
            list of tuples: A list containing tuples with (fish_id, fish_name)
                            or an empty list if no fish are found.
        """
        cursor = connection.cursor()

        query = """
        SELECT dp.fish_id, ft.name
        FROM daily_pond dp
        JOIN fish_types ft ON dp.fish_id = ft.fish_id
        WHERE dp.user_id = %s
        AND dp.expires_at > current_date;
        """

        try:
            cursor.execute(query, (user_id,))
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return result
        except Exception as err:
            cursor.close()
            connection.close()
            print(f"There was an error getting the user's pond: {err}")
            traceback.print_exc()
            return None

    @staticmethod
    def insert_fish_into_daily_pond(connection, user_id, fish_ids):
        """
        Adds multiple fish to the user's daily pond.

        Args:
            connection: psycopg2 connection object
            user_id (str): Discord user ID
            fish_ids (list of int): List of fish_id values to add

        Returns:
            bool: True if insert was successful, False otherwise
        """

        cursor = connection.cursor()

        query = """
        INSERT INTO daily_pond (user_id, fish_id)
        VALUES %s;
        """
        values = [(user_id, fish_id) for fish_id in fish_ids]

        try:
            execute_values(cursor, query, values)

            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as err:
            cursor.close()
            connection.close()
            print(f"There was an error inserting fish into the user's pond: {err}")
            traceback.print_exc()
            return False

    @staticmethod
    def insert_fish(connection, name: str, rarity: str, catch_rate: float):
        """ "
        Adds a new fish type to the DB

        Args:
            name (str): fish name
            rarity (str): fish's rarity (COMMON, UNCOMMON, RARE or EXOTIC)
            catch_rate (float): the fish's base catch rate (from 0 to 1)

        Returns:
            bool: True if was inserted correctly, False otherwise
        """
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
            return False

        cursor.close()
        connection.close()
        return True

    @staticmethod
    def sample_fish_from_rarity(connection, rarity: str):
        """
        Samples a random fish from the given rarity

        Args:
            str: rarity. 'common', 'uncommon', 'rare' or 'exotic'

        Returns:
            int: Sampled fish's fish_id
        """
        cursor = connection.cursor()
        try:
            # Get a random fish of the chosen rarity
            cursor.execute(
                "SELECT fish_id FROM fish_types WHERE rarity = %s ORDER BY RANDOM() LIMIT 1",
                (rarity,),
            )
            record = cursor.fetchone()
            fish = record[0]
            print(f"Read successful. fish_id = {fish}")
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
