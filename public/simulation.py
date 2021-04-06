# STL
from datetime import datetime, timedelta, time
import logging
from random import randint, choice, shuffle
from pprint import pprint

# Pip
from pyowm.owm import OWM

# Local
from .scripts import create_datetime_ID, fetch
from .calculate import celsius_to_fahrenheit, fahrenheit_to_celsius
from .person import Person
from .schedule_builder import construct_schedule, get_action_time
from .smart_home import SmartHome
from .local_config import API_key

owm = OWM(API_key)
mgr = owm.weather_manager()

# Define the simulation class by initializing state of the smart home and household members
class Simulation(object):

    def __init__(self, smart_home):
        weather = self.get_current_weather()
        self.smart_home = smart_home
        self.current_time = datetime.now()
        self.last_weather_update = datetime.now()
        self.generation_mode = False
        self.ext_temps = {}
        self.current_temp = weather.temperature('fahrenheit')["temp"]
        self.weather_main = weather.status
        self.weather_desc = weather.detailed_status
        self.person_sim = True
        self.residents = [
            Person(self, "Jet", True, "Bedroom_1", "Bathroom_1"),
            Person(self, "Spike", True, "Bedroom_1", "Bathroom_1"),
            Person(self, "Faye", False, "Bedroom_2", "Bathroom_2"),
            Person(self, "Ed", False, "Bedroom_3", "Bathroom_2")
        ]
        self.auto_resolve = []  # Contains tuples of events to resolve in (dt, target_comp)
        self.temp_delta = 0
        self.water_to_heat = 0
        self.debug = smart_home.debug
        self.debug_temp = False
        self.debug_weather = False
        self.sim_speed = 1

    # Resolve household member tasks 
    def resolve_tasks(self):
        for resident in self.residents:
            if self.current_time == resident.resolve_time:
                resident.occupied = False
                resident.resolve_time = None
                resident.comp_occupied.disengage()
            for event in resident.schedule:  # Event structure: tuple(datetime of event, function to be called, parameters to be passed to function)
                if event[0]  == self.current_time:
                    event[1](*event[2])  # Refers to the stored function(index 1) and parameters(index 2) in the tuple and calls fxn with params
        resolved = []
        for task in self.auto_resolve:
            if self.current_time == task[0]:
                task[1].disengage()
                resolved.append(task)
        if len(resolved) > 0:
            self.auto_resolve = [task for task in self.auto_resolve if task not in resolved]
    
    # Move resident to random room
    def random_move(self):
        if randint(0, 1000) == 0:
            resident = choice(self.residents)
            if not resident.occupied:
                rooms = ["Kitchen", "Living_Room", "Garage"]
                rooms.extend([resident.bathroom, resident.bedroom])
                resident.move_to(choice(rooms))

    ## Resident opens random window
    def random_window(self):
        if randint(0, 2000) == 0:
            resident = choice(self.residents)
            if not resident.occupied:
                resident.open_windows()

    def handle_random_events(self):
        self.random_move()
        self.random_window()
    
    ## Resident is asleep
    def sleep_mode(self):
        for comp in self.smart_home.windows:
            comp.disengage()
        for comp in self.smart_home.lights:
            comp.disengage()

    ## Update indoor temperature based on outdoor temperature and HVAC functionality
    def update_temp_delta(self):
        temp_diff = self.current_temp - self.smart_home.int_temp
        temp_delta = temp_diff * (0.2/3600)
        for door in self.smart_home.ext_doors:
            if door.engaged:
                temp_delta += temp_diff * (0.2/300)
        for window in self.smart_home.windows:
            if window.engaged:
                temp_delta += temp_diff * (0.1/300)
        if self.smart_home.components["hvac_01"].engaged:
            if self.smart_home.thermostat.mode == "cool":
                temp_delta -= 1/60
            else:
                temp_delta += 1/60
        self.temp_delta = temp_delta

    ## Check updated temperature on thermostat
    def check_thermostat(self):
        self.update_temp_delta()
        self.smart_home.int_temp += self.temp_delta
        self.smart_home.thermostat.check_temp()

    ## Update water to heat based on heater functionality
    def check_water_heater(self):
        WH = self.smart_home.components["water-heater_01"]
        if not WH.engaged and self.water_to_heat > 0:
            WH.engage()
        elif WH.engaged and self.water_to_heat <= 0:
            WH.disengage()
            self.water_to_heat = 0
        elif WH.engaged:
            self.water_to_heat -= 0.25/60
    
    ## Fetch current weather data
    def get_current_weather(self):
        # return mgr.one_call(lat=33.5020, lon=-86.8064, exclude="minute,hourly,daily", units="imperial")
        return mgr.weather_at_coords(lon=-86.80249, lat=33.52066).weather

    ## Update weather data
    def update_weather(self):
        if not self.debug_weather or not self.debug_temp:
            weather = self.get_current_weather()
            self.last_weather_update = datetime.now()
            if not self.debug_temp:
                self.current_temp = weather.temperature('fahrenheit')["temp"]
            if not self.debug_weather:
                self.weather_main = weather.status
                self.weather_desc = weather.detailed_status

    ## Get external temperature
    def fetch_ext_temp(self):
        try:
            self.current_temp = celsius_to_fahrenheit(self.ext_temps[create_datetime_ID(self.current_time)]["temp"])
        except KeyError:
            self.current_temp = self.current_temp
        return self.current_temp

    ## Generate schedules for household members
    def build_schedules(self):
        adult_schedules = ["01", "02"]
        child_schedules = ["01", "02"]
        shuffle(adult_schedules)
        shuffle(child_schedules)
        for resident in self.residents:
            resident.schedule.clear()
            if resident.adult:
                schedule_number = adult_schedules.pop()
            else:
                schedule_number = child_schedules.pop()
            construct_schedule(resident, schedule_number)

    ## Perform tasks based on schedule
    def handle_regular_tasks(self):
        self.smart_home.current_time = self.current_time
        self.current_temp = self.fetch_ext_temp()
        if self.person_sim:
            if self.current_time.time() == time(0):
                self.build_schedules()
            elif self.current_time.time() == time(20, 30):
                self.sleep_mode()
            self.handle_random_events()
            self.resolve_tasks()
        self.check_thermostat()
        self.check_water_heater()

    ## Establish the initial state of the simulation
    def init_sim_state(self):
        self.current_time = datetime.now()
        self.last_weather_update = datetime.now()
        self.current_temp = self.get_current_weather().temperature('fahrenheit')["temp"]
        self.temp_delta = 0
        self.water_to_heat = 0

    ## Increment time for continuous simulation
    def increment_time(self):
        for _ in range(self.sim_speed):
            self.current_time += timedelta(seconds=1)
            self.smart_home.current_time = self.current_time
            if self.current_time - self.last_weather_update > timedelta(seconds=15):
                self.update_weather()
            self.check_thermostat()
            self.check_water_heater()
    
    ## Same as above except for seconds
    def increment_second(self):
        self.handle_regular_tasks()
        self.current_time += timedelta(seconds=1)
        if not self.smart_home.debug:
            if self.current_time.time().hour == 23 and self.current_time.time().minute == 59 and self.current_time.time().second == 59:
                self.smart_home.db_conn.writeDailyUsage(self.current_time.date())
    
    ## Begin the simulation
    def simulate(self, td: timedelta):
        self.generation_mode = True
        now = datetime.now()
        end_person_sim = datetime.now()
        end_person_sim = end_person_sim.replace(hour=0, minute=0, second=0, microsecond=0)
        time = now - td
        self.current_time = datetime(time.year, time.month, time.day, 0, 0, 0)
        self.smart_home.current_time = self.current_time
        self.ext_temps = fetch(start=self.current_time)
        self.smart_home.components["ref_01"].engage()
        while self.current_time < now:
            if self.current_time == end_person_sim:
                self.person_sim = False
                self.auto_resolve = []
            self.increment_second()
        print("Data generation complete!")
        if not self.smart_home.debug:
            self.smart_home.db_conn.doProjection(self.current_time.date())
        self.generation_mode = False
