import psycopg2
import os
import traceback
from dotenv import load_dotenv

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
    def insert_fish(connection, name: str, rarity: str, catch_rate: float):
        cursor = connection.cursor()
        # Insert fish if it's not in the table already
        query = """
        INSERT INTO fish_list (name, rarity, catch_rate) 
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
                "SELECT name FROM fish_list WHERE rarity = %s ORDER BY RANDOM() LIMIT 1",
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
