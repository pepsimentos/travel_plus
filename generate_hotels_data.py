import random
from datetime import datetime, timedelta
import sqlite3

# Database connection
DB_NAME = 'db.sqlite3'

# Set to track unique hotel IDs
used_hotel_ids = set()

def generate_hotel_id():
    while True:
        hotel_id = f"HT-{random.randint(10000, 99999)}"
        if hotel_id not in used_hotel_ids:
            used_hotel_ids.add(hotel_id)
            return hotel_id

def generate_random_date():
    start_date = datetime.now().date() + timedelta(days=random.randint(1, 30))
    end_date = start_date + timedelta(days=random.randint(1, 14))
    return start_date, end_date

def generate_room_type():
    return random.choice(["Single", "Double", "Suite", "Deluxe"])

def generate_hotel_data(cities, num_hotels_per_city=5):
    hotels = []

    for city in cities:
        for _ in range(num_hotels_per_city):
            start_stay, end_stay = generate_random_date()
            hotel = {
                "hotel_id": generate_hotel_id(),
                "hotel_city": city,
                "start_stay": start_stay,
                "end_stay": end_stay,
                "room_type": generate_room_type(),
                "available_rooms": random.randint(10, 100),
            }
            hotels.append(hotel)

    return hotels

def insert_hotels_into_db(hotels):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    for hotel in hotels:
        cursor.execute(
            """
            INSERT INTO hotel (
                hotel_id, hotel_city, start_stay, end_stay, room_type, available_rooms
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                hotel["hotel_id"], hotel["hotel_city"], hotel["start_stay"],
                hotel["end_stay"], hotel["room_type"], hotel["available_rooms"]
            ),
        )

    connection.commit()
    connection.close()

def main():
    cities = [
        "Paris", "London", "Istanbul", "Dubai", "New York", "Tokyo", "Sydney", "Berlin", "Rome", "Amsterdam",
        "Bangkok", "Moscow", "Cape Town", "Rio de Janeiro", "Los Angeles", "Singapore", "Hong Kong", "Cairo", "Madrid", "Toronto",
        "Mexico City", "Mumbai", "Seoul", "Buenos Aires", "Johannesburg", "Zurich", "Vienna", "Stockholm", "Kuala Lumpur", "Lima"
    ]
    hotels = generate_hotel_data(cities)
    insert_hotels_into_db(hotels)
    print(f"Generated and inserted {len(hotels)} hotels into the database.")

if __name__ == "__main__":
    main()
