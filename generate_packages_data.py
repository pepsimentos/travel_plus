import random
from datetime import datetime, timedelta
import sqlite3

# Database connection
DB_NAME = 'db.sqlite3'

# Set to track unique package IDs
used_package_ids = set()

def generate_package_id():
    while True:
        package_id = f"PK-{random.randint(10000, 99999)}"
        if package_id not in used_package_ids:
            used_package_ids.add(package_id)
            return package_id

def generate_random_dates():
    start_date = datetime.now().date() + timedelta(days=random.randint(1, 30))
    end_date = start_date + timedelta(days=random.randint(3, 10))
    return start_date, end_date

def generate_package_price():
    return round(random.uniform(300, 5000), 2)  # Prices range from $300 to $5000

def generate_packages_data(cities, agents, num_packages_per_city=5):
    packages = []

    for city in cities:
        for _ in range(num_packages_per_city):
            pkg_start_date, pkg_end_date = generate_random_dates()
            package = {
                "package_id": generate_package_id(),
                "pkg_destination": city,
                "pkg_start_date": pkg_start_date,
                "pkg_end_date": pkg_end_date,
                "package_price": generate_package_price(),
                "agent": random.choice(agents) if agents else None,  # Assign a random agent if available
            }
            packages.append(package)

    return packages

def insert_packages_into_db(packages):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    for package in packages:
        cursor.execute(
            """
            INSERT INTO package (
                package_id, pkg_start_date, pkg_end_date, package_price, pkg_destination, agent_id
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                package["package_id"], package["pkg_start_date"], package["pkg_end_date"],
                package["package_price"], package["pkg_destination"], package["agent"]
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

    # Example list of agent IDs fetched from the database
    agents = ["AG-10001", "AG-10002", "AG-10003", "AG-10004"]  # Replace with actual agent IDs from your database

    packages = generate_packages_data(cities, agents)
    insert_packages_into_db(packages)
    print(f"Generated and inserted {len(packages)} packages into the database.")

if __name__ == "__main__":
    main()
