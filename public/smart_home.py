# STL
from datetime import timedelta, datetime
import logging

# PIP
import psycopg2

# Local
from .components import Sensor
from .components import Appliance
from .components import Thermostat
from .smarthome_builder import build_home
from .db import DBWriter

logging.basicConfig(filename="LOG.txt", level=logging.INFO, filemode="w")

# Define the smart home class and establish it's state
class SmartHome(object):

    def __init__(self, debug=False):
        # self.db_conn = psycopg2.connect(database = "Team1DB", user = "Team1", password = "1Team1", host = "164.111.161.243", port = "5432")
        self.debug = debug
        self.db_conn = None
        if not debug:
            self.db_conn = DBWriter()
        self.current_time = datetime.now()
        self.int_temp = 70
        self.thermostat = None
        self.components = {}
        self.rooms = {
            "Bedroom_1": [],
            "Bedroom_2": [],
            "Bedroom_3": [],
            "Bathroom_1": [],
            "Bathroom_2": [],
            "Living_Room": [],
            "Kitchen": [],
            "Garage": []
        }
        self.appliances = []
        self.lights = []
        self.ext_doors = []
        self.other_doors = []
        self.windows = []
        self.baths = []
        self.init_components()

# Ititialize the components within the smarthome
    def init_components(self):
        components = {
            "appliances": (self.appliances, Appliance),
            "lights": (self.lights, Appliance),
            "ext_doors": (self.ext_doors, Sensor),
            "other_doors": (self.other_doors, Sensor),
            "windows": (self.windows, Sensor),
            "baths": (self.baths, Sensor)
            }
        for k, v in components.items():
            for comp in build_home(self.db_conn)[k]:
                component = v[1](self, *comp)
                self.components[component.comp_id] = component
                room_id = component.name.split()[0]
                if room_id in self.rooms:
                    self.rooms[room_id].append(component)
                v[0].append(component)
        self.thermostat = Thermostat(self, self.components["hvac_01"])
