# STL
from datetime import timedelta, time, datetime
from random import randint, random
import logging


def get_action_time(lower: time, upper: time, today: datetime.date):
    lower = datetime(today.year, today.month, today.day, lower.hour, lower.minute, lower.second)
    upper = datetime(today.year, today.month, today.day, upper.hour, upper.minute, upper.second)
    out = lower + timedelta(seconds=randint(0, (upper-lower).total_seconds()))
    return out


class Person(object):

    def __init__(self, simulation, name: str, adult: bool, bedroom: str, bathroom: str):
        self.simulation = simulation
        self.name = name
        self.adult = adult
        self.bedroom = bedroom
        self.bathroom = bathroom
        self.location = bedroom
        self.schedule = []
        self.occupied = True
        self.comp_occupied = None
        self.resolve_time = None
        self.temperature = 0
        self.departure = time(7, 30, 0, 0)
        if adult:
            self.waketime = time(5, 0, 0, 0)
            self.bedtime = time(22, 30, 0, 0)
            self.arrival = time(17, 30, 0, 0)
        else:
            self.waketime = time(6, 0, 0, 0)
            self.bedtime = time(20, 30, 0, 0)
            self.arrival = time(16, 0, 0, 0)

    def set_occupied(self, occupied: bool):
        self.occupied = occupied

    def wake_up(self):
        self.occupied = False
        for device in self.simulation.smart_home.rooms[self.bedroom]:
            if device.comp_id.split("_")[0] == "light":
                device.engage()

    def sleep(self):
        self.move_to(self.bedroom)
        self.temperature = self.take_temperature()
        for device in self.simulation.smart_home.rooms[self.bedroom]:
            if device.comp_id.split("_")[0] in ["light", "window"]:
                device.disengage()
        self.occupied = True

    def perform_action(self, duration: timedelta, location: str, target, occupying: bool=True):
        self.move_to(location)
        target.engage()
        if occupying:
            self.occupied = True
            self.comp_occupied = target
            self.resolve_time = self.simulation.current_time + duration
        else:
            self.simulation.auto_resolve.append((self.simulation.current_time + duration, target))

    def shower(self, duration: timedelta=timedelta(minutes=5)):
        target_id = "bath_0" + self.bathroom.split("_")[1]
        target = self.simulation.smart_home.components[target_id]
        self.perform_action(duration, self.bathroom, target)
        self.simulation.water_to_heat += (25*.65)

    def bath(self, duration: timedelta=timedelta(minutes=20)):
        target_id = "bath_0" + self.bathroom.split("_")[1]
        target = self.simulation.smart_home.components[target_id]
        self.perform_action(duration, self.bathroom, target)
        self.simulation.water_to_heat += (30*.65)

    def microwave(self, duration: timedelta=timedelta(minutes=5)):
        target_comp = self.simulation.smart_home.components["microwave_01"]
        self.perform_action(duration, "Kitchen", target_comp, False)

    def stove(self, duration: timedelta=timedelta(minutes=15)):
        target_comp = self.simulation.smart_home.components["stove_01"]
        self.perform_action(duration, "Kitchen", target_comp)

    def oven(self, duration: timedelta=timedelta(minutes=45)):
        target_comp = self.simulation.smart_home.components["oven_01"]
        self.perform_action(duration, "Kitchen", target_comp, False)

    def dishwasher(self, duration: timedelta=timedelta(minutes=45)):
        target_comp = self.simulation.smart_home.components["dishwasher_01"]
        self.perform_action(duration, "Kitchen", target_comp, False)
        self.simulation.water_to_heat += 6

    def clothes_washer(self, duration: timedelta=timedelta(minutes=30)):
        target_comp = self.simulation.smart_home.components["clothes-washer_01"]
        self.perform_action(duration, "Garage", target_comp, False)
        self.simulation.water_to_heat += (20*.85)

    def clothes_dryer(self, duration: timedelta=timedelta(minutes=30)):
        target_comp = self.simulation.smart_home.components["clothes-dryer_01"]
        self.perform_action(duration, "Garage", target_comp, False)

    def tv(self, tv_id: str, duration: timedelta=timedelta(hours=4)):
        target_comp = self.simulation.smart_home.components[tv_id]
        if tv_id == "tv_01":
            location = "Bedroom_1"
            duration = timedelta(hours=2)
        else:
            location = "Living_Room"
        self.perform_action(duration, location, target_comp, False)

    def enter_house(self, door_id: str, duration: timedelta=timedelta(seconds=30)):
        target_comp = self.simulation.smart_home.components[door_id]
        if door_id == "door_3":
            location = "Kitchen"
        else:
            location = "Living_Room"
        self.perform_action(duration, location, target_comp)

    def exit_house(self, door_id: str, duration: timedelta=timedelta(seconds=30)):
        target_comp = self.simulation.smart_home.components[door_id]
        if door_id == "door_3":
            location = "Kitchen"
        else:
            location = "Living_Room"
        self.perform_action(duration, location, target_comp, False)
        self.location = "out"
    
    def leave_and_return(self, door_id: str, time_gone: timedelta, door_duration: timedelta=timedelta(seconds=30)):
        self.exit_house(door_id, door_duration)
        self.occupied = True
        self.location = "out"
        self.schedule.append((self.simulation.current_time + time_gone, Person.enter_house, (self, door_id)))

    def go_outside(self, door_id: str):
        time_gone = timedelta(minutes=randint(5, 15))
        self.leave_and_return(door_id, time_gone)

    def go_to_work_or_school(self, door_id: str):
        if self.adult:
            time_gone = timedelta(hours=10, minutes=randint(0, 10))
        else:
            time_gone = timedelta(hours=8, minutes=randint(25, 35))
        self.leave_and_return(door_id, time_gone)

    def open_windows(self):
        duration = timedelta(minutes=randint(5, 60))
        for comp in self.simulation.smart_home.rooms[self.location]:
            if comp.comp_id.split("_")[0] == "window":
                self.perform_action(duration, self.location, comp, False)

    def move_to(self, room: str):
        if self.location == room:
            return
        turn_off = True
        for resident in self.simulation.residents:
            if resident != self and resident.location == self.location:
                turn_off = False
                break
        if turn_off and self.location != "out":
            for device in self.simulation.smart_home.rooms[self.location]:
                if device.comp_id.split("_")[0] in ["light", "fan"]:
                    device.disengage()
        self.location = room
        if room != "out":
            for device in self.simulation.smart_home.rooms[room]:
                if device.comp_id.split("_")[0] in ["light", "fan"]:
                    device.engage()

    def take_temperature(self):
        var = random() * 3
        self.temperature = 96.5 + var   ## 96.5-100
        self.simulation.smart_home.db_conn.writeTemp(self.name, self.temperature, self.simulation.current_time.date())
