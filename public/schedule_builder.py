# STL
from datetime import datetime, timedelta, time
from random import randint

# Local
from .person import Person, get_action_time

# Define one hour in terms of time change
ONE_HOUR = timedelta(minutes=60)

# Define several schedule options for each member of the household
SCHEDULES = {
    "child_weekday_01": [
        ((5, 50), (6, 10), Person.wake_up, tuple()),
        ((6, 10), (6, 20), Person.bath, tuple()),
        ((6, 40), (6, 45), Person.microwave, tuple()),
        ((7, 25), (7, 30), Person.go_to_work_or_school, ("door_01",)),
        ((16, 10), (16, 30), Person.tv, ("tv_02",)),
        ((17, 0), (17, 30), Person.go_outside, ("door_02",)),
        ((20, 20), (20, 40), Person.sleep, tuple())
    ],
    "child_weekday_02": [
        ((5, 50), (6, 10), Person.wake_up, tuple()),
        ((6, 40), (6, 50), Person.shower, tuple()),
        ((6, 50), (6, 55), Person.microwave, tuple()),
        ((7, 31), (7, 33), Person.go_to_work_or_school, ("door_01",)),
        ((16, 10), (16, 30), Person.go_outside, ("door_02",)),
        ((20, 20), (20, 40), Person.sleep, tuple())
    ],
    "child_weekend_01": [
        ((5, 50), (6, 10), Person.wake_up, tuple()),
        ((6, 40), (6, 50), Person.shower, tuple()),
        ((7, 0), (7, 15), Person.microwave, tuple()),
        ((7, 30), (8, 0), Person.tv, ("tv_02",)),
        ((9, 30), (10, 0), Person.go_outside, ("door_01",)),
        ((12, 30), (13, 0), Person.microwave, tuple()),
        ((13, 30), (14, 0), Person.go_outside, ("door_02",)),
        ((15, 5), (15, 30), Person.go_outside, ("door_03",)),
        ((16, 10), (16, 30), Person.go_outside, ("door_02",)),
        ((17, 30), (17, 50), Person.bath, tuple()),
        ((20, 20), (20, 40), Person.sleep, tuple())
    ],
    "child_weekend_02": [
        ((5, 50), (6, 10), Person.wake_up, tuple()),
        ((6, 15), (6, 30), Person.shower, tuple()),
        ((6, 40), (6, 55), Person.microwave, tuple()),
        ((8, 30), (9, 0), Person.go_outside, ("door_02",)),
        ((10, 30), (11, 0), Person.go_outside, ("door_02",)),
        ((13, 0), (14, 0), Person.microwave, tuple()),
        ((14, 30), (15, 0), Person.go_outside, ("door_03",)),
        ((16, 32), (16, 45), Person.go_outside, ("door_02",)),
        ((17, 0), (17, 25), Person.tv, ("tv_02",)),
        ((20, 20), (20, 40), Person.sleep, tuple())
    ],
    "adult_weekday_01": [
        ((4, 50), (5, 10), Person.wake_up, tuple()),
        ((5, 10), (5, 20), Person.bath, tuple()),
        ((5, 40), (5, 45), Person.microwave, tuple()),
        ((5, 50), (6, 20), Person.stove, tuple()),
        ((7, 25), (7, 30), Person.go_to_work_or_school, ("door_03",)),
        ((17, 50), (18, 0), Person.go_outside, ("door_03",)),
        ((18, 20), (18, 40), Person.tv, ("tv_01",)),
        ((20, 20), (20, 40), Person.sleep, tuple())
    ],
    "adult_weekday_02": [
        ((4, 50), (5, 10), Person.wake_up, tuple()),
        ((5, 15), (5, 30), Person.microwave, tuple()),
        ((5, 40), (5, 50), Person.shower, tuple()),
        ((7, 31), (7, 35), Person.go_to_work_or_school, ("door_03",)),
        ((17, 50), (18, 0), Person.go_outside, ("door_01",)),
        ((18, 20), (18, 40), Person.oven, tuple()),
        ((20, 20), (20, 40), Person.sleep, tuple())
    ],
    "adult_weekend_01": [
        ((4, 50), (5, 10), Person.wake_up, tuple()),
        ((5, 15), (5, 30), Person.microwave, tuple()),
        ((5, 40), (5, 50), Person.shower, tuple()),
        ((6, 0), (6, 30), Person.tv, ("tv_01",)),
        ((6, 40), (7, 0), Person.clothes_washer, tuple()),
        ((7, 30), (7, 45), Person.clothes_dryer, tuple()),
        ((8, 30), (9, 0), Person.go_outside, ("door_03",)),
        ((10, 0), (10, 30), Person.dishwasher, tuple()),
        ((11, 5), (12, 30), Person.go_outside, ("door_02",)),
        ((14, 0), (15, 30), Person.go_outside, ("door_01",)),
        ((17, 50), (18, 0), Person.go_outside, ("door_03",)),
        ((18, 20), (18, 40), Person.oven, (ONE_HOUR,)),
        ((19, 40), (20, 0), Person.bath, tuple()),
        ((20, 20), (20, 40), Person.sleep, tuple())
    ],
    "adult_weekend_02": [
        ((4, 50), (5, 10), Person.wake_up, tuple()),
        ((5, 10), (5, 30), Person.shower, tuple()),
        ((5, 35), (5, 50), Person.microwave, tuple()),
        ((5, 50), (6, 40), Person.stove, tuple()),
        ((7, 0), (7, 30), Person.dishwasher, tuple()),
        ((8, 30), (9, 0), Person.go_outside, ("door_01",)),
        ((11, 0), (12, 30), Person.go_outside, ("door_03",)),
        ((13, 0), (13, 15), Person.clothes_washer, tuple()),
        ((13, 45), (14, 0), Person.clothes_dryer, tuple()),
        ((14, 0), (14, 25), Person.go_outside, ("door_03",)),
        ((16, 0), (16, 30), Person.stove, tuple()),
        ((17, 50), (18, 0), Person.go_outside, ("door_01",)),
        ((18, 0), (18, 30), Person.tv, ("tv_01",)),
        ((20, 20), (20, 40), Person.sleep, tuple())
    ],
}

# Construct schedule for the passed in member of the household
def construct_schedule(person: Person, schedule_number: str):
    current_time = person.simulation.current_time
    today = current_time.date()
    weekday = current_time.isoweekday()
    key = ""
    if person.adult:
        key += "adult_"
    else:
        key += "child_"
    if weekday <= 5:
        key += "weekday_"
    else:
        key += "weekend_"
    key += schedule_number
    for details in SCHEDULES[key]:
        action_time = get_action_time(time(*details[0]), time(*details[1]), today)
        func = details[2]
        params = (person, *details[3])
        person.schedule.append((action_time, func, params))
