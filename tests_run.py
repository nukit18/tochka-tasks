import pytest
from datetime import datetime, timedelta
from run import check_capacity


def test_quests_under_max_capacity():
    """Тесты, когда гости вмещаются в отель."""
    max_capacity = 3
    multiple_guests_list = [
        [
            {"name": "1", "check-in": "2021-01-10", "check-out": "2021-01-15"},
            {"name": "2", "check-in": "2021-01-12", "check-out": "2021-01-20"},
            {"name": "3", "check-in": "2021-01-15", "check-out": "2021-01-21"},
        ],
        [
            {"name": "1", "check-in": "2021-01-10", "check-out": "2021-06-15"},
            {"name": "2", "check-in": "2021-03-12", "check-out": "2021-04-20"},
            {"name": "3", "check-in": "2021-05-15", "check-out": "2021-10-21"},
        ],
        [
            {"name": "1", "check-in": "2021-01-10", "check-out": "2021-01-15"},
            {"name": "2", "check-in": "2021-02-12", "check-out": "2021-02-20"},
            {"name": "3", "check-in": "2021-03-15", "check-out": "2021-03-21"},
        ]
    ]
    for guests_list in multiple_guests_list:
        assert check_capacity(max_capacity, guests_list) == True


def test_over_capacity():
    """Тест, когда гостей больше, чем максимальная вместимость."""
    max_capacity = 2

    multiple_guests_list = [
        [
            {"name": "1", "check-in": "2021-01-10", "check-out": "2021-01-16"},
            {"name": "2", "check-in": "2021-01-12", "check-out": "2021-01-20"},
            {"name": "3", "check-in": "2021-01-15", "check-out": "2021-01-21"},
        ],
        [
            {"name": "1", "check-in": "2021-01-10", "check-out": "2021-01-16"},
            {"name": "2", "check-in": "2021-01-10", "check-out": "2021-01-20"},
            {"name": "3", "check-in": "2021-01-10", "check-out": "2021-01-21"},
        ]
    ]
    for guests_list in multiple_guests_list:
        assert check_capacity(max_capacity, guests_list) == False


def test_empty_guests():
    """Тест, когда гостей нет."""
    max_capacity = 2
    guests = []
    assert check_capacity(max_capacity, guests) == True


def test_large_date_range():
    """Тест на большом временном промежутке с множеством бронирований."""
    max_capacity = 10
    guests = []
    start_date = datetime(2023, 1, 1)
    for i in range(10):
        check_in = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        check_out = (start_date + timedelta(days=i + 3)).strftime("%Y-%m-%d")
        guests.append({"check-in": check_in, "check-out": check_out})
    assert check_capacity(max_capacity, guests) == True


def generate_large_guest_list(n_guests, overlapping=False):
    """Генерация большого списка гостей (10^5 записей)."""
    guests = []
    start_date = datetime(2025, 1, 1)
    for i in range(n_guests):
        check_in = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        check_out = (start_date + timedelta(days=i + (2 if overlapping else 1))).strftime("%Y-%m-%d")
        print(check_in, check_out)
        guests.append({"check-in": check_in, "check-out": check_out})
    return guests


def test_large_scale_success():
    """Тест на 10^5 гостей без пересечений (успешное заселение)."""
    max_capacity = 1
    n_guests = 10**5
    guests = generate_large_guest_list(n_guests, overlapping=False)
    assert check_capacity(max_capacity, guests) == True


def test_large_scale_failure():
    """Тест на 10^5 гостей с пересечениями (неуспешное заселение)."""
    max_capacity = 1
    n_guests = 10**5
    guests = generate_large_guest_list(n_guests, overlapping=True)
    assert check_capacity(max_capacity, guests) == False
