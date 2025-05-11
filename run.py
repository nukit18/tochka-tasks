
import json
from datetime import datetime, timedelta
from typing import Dict, List


def check_capacity(max_capacity: int, guests: List[Dict[str, str]]) -> bool:
    date_format = "%Y-%m-%d"
    booking_actions = []
    for booking_info in guests:
        check_in = datetime.strptime(booking_info["check-in"], date_format)
        check_out = datetime.strptime(booking_info["check-out"], date_format)
        booking_actions.append((check_in, 1))
        booking_actions.append((check_out, -1))

    booking_actions.sort(key=lambda x: (x[0], x[1]))

    current_guests = 0
    for booking_date, action in booking_actions:
        current_guests += action
        if current_guests > max_capacity:
            return False
    return True


if __name__ == "__main__":
    max_capacity = int(input())
    n = int(input())


    guests = []
    for _ in range(n):
        guest_json = input()
        guest_data = json.loads(guest_json)
        guests.append(guest_data)


    result = check_capacity(max_capacity, guests)
    print(result)