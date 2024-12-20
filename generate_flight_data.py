import random
from datetime import datetime, timedelta
import sqlite3

# Database connection
DB_NAME = 'db.sqlite3'  # Change this if your SQLite database file has a different name

# Set to track unique flight IDs
used_flight_ids = set()

def generate_random_time():
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    return f"{hour:02}:{minute:02}:00"

def generate_flight_id():
    while True:
        flight_id = f"FL-{random.randint(10000, 99999)}"
        if flight_id not in used_flight_ids:
            used_flight_ids.add(flight_id)
            return flight_id

def generate_flight_number():
    return f"{random.choice(['ME', 'AF', 'DL', 'EK'])}{random.randint(1000, 9999)}"

def generate_flight_data(source, destinations, num_days=10):
    going_flights = []
    returning_flights = []

    for destination in destinations:
        for day in range(num_days):
            flight_date = datetime.now().date() + timedelta(days=day)
            takeoff_time = generate_random_time()
            landing_time = generate_random_time()

            # Flight to destination
            flight_to = {
                "flight_id": generate_flight_id(),
                "flight_number": generate_flight_number(),
                "start_city": source,
                "end_city": destination,
                "takeoff_time": takeoff_time,
                "landing_time": landing_time,
                "flight_date": flight_date,
                "flight_class": random.choice(["Economy", "Business", "First"]),
                "available_seats": random.randint(50, 300),
            }

            # Flight back to source
            flight_back = {
                "flight_id": generate_flight_id(),
                "flight_number": generate_flight_number(),
                "start_city": destination,
                "end_city": source,
                "takeoff_time": generate_random_time(),
                "landing_time": generate_random_time(),
                "flight_date": flight_date,
                "flight_class": random.choice(["Economy", "Business", "First"]),
                "available_seats": random.randint(50, 300),
            }

            going_flights.append(flight_to)
            returning_flights.append(flight_back)

    return going_flights, returning_flights

def insert_flights_into_db(flights):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    for flight in flights:
        cursor.execute(
            """
            INSERT INTO flight (
                flight_id, flight_number, start_city, end_city, takeoff_time,
                landing_time, flight_date, flight_class, available_seats
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                flight["flight_id"], flight["flight_number"], flight["start_city"],
                flight["end_city"], flight["takeoff_time"], flight["landing_time"],
                flight["flight_date"], flight["flight_class"], flight["available_seats"]
            ),
        )

    connection.commit()
    connection.close()

def main():
    source = "Beirut"
    destinations = [
        "Paris", "London", "Istanbul", "Dubai", "New York", "Tokyo", "Sydney", "Berlin", "Rome", "Amsterdam",
        "Bangkok", "Moscow", "Cape Town", "Rio de Janeiro", "Los Angeles", "Singapore", "Hong Kong", "Cairo", "Madrid", "Toronto",
        "Mexico City", "Mumbai", "Seoul", "Buenos Aires", "Johannesburg", "Zurich", "Vienna", "Stockholm", "Kuala Lumpur", "Lima"
    ]
    going_flights, returning_flights = generate_flight_data(source, destinations)

    insert_flights_into_db(going_flights + returning_flights)  # To insert data into the database

    print(f"Generated {len(going_flights)} going flights and {len(returning_flights)} returning flights.")

if __name__ == "__main__":
    main()
