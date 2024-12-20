from django.core.management.base import BaseCommand
from datetime import datetime, timedelta, time
import random
from users.models import Flight

# Plane types and seat capacities
PLANE_SEATS = {"Small": 70, "Medium": 160, "Large": 300}

class Command(BaseCommand):
    help = "Generate outbound and return flights with logical data"

    def handle(self, *args, **kwargs):
        cities = ["Paris", "London", "Dubai", "Istanbul", "Athens", "New York", "Tokyo"]
        beirut = "Beirut"

        for city in cities:
            plane_type = random.choice(list(PLANE_SEATS.keys()))
            seats = PLANE_SEATS[plane_type]

            outbound_date = datetime.now() + timedelta(days=random.randint(1, 30))
            Flight.objects.create(
                flight_number=f"OUT-{city[:3].upper()}-{random.randint(100, 999)}",
                start_city=beirut,
                end_city=city,
                flight_date=outbound_date.date(),
                takeoff_time=time(10, 0),  # Correct format: 10:00
                landing_time=time(14, 0),  # Correct format: 14:00 (2 PM)
                available_seats=seats,
            )

            return_date = outbound_date + timedelta(days=random.randint(1, 7))
            Flight.objects.create(
                flight_number=f"RET-{city[:3].upper()}-{random.randint(100, 999)}",
                start_city=city,
                end_city=beirut,
                flight_date=return_date.date(),
                takeoff_time=time(16, 0),  # Correct format: 16:00 (4 PM)
                landing_time=time(20, 0),  # Correct format: 20:00 (8 PM)
                available_seats=seats,
            )

        # Special flight for testing overbooking
        Flight.objects.create(
            flight_number="TEST-1SEAT",
            start_city=beirut,
            end_city="London",
            flight_date=datetime.now().date() + timedelta(days=2),
            takeoff_time=time(6, 0),  # Correct format: 6:00 AM
            landing_time=time(10, 0),  # Correct format: 10:00 AM
            available_seats=1,
        )

        self.stdout.write(self.style.SUCCESS("Dummy flights generated successfully!"))
