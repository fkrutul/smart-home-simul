import logging

from .sensor import Sensor

class Appliance(Sensor):

    def __init__(self, smart_home, db_conn, comp_id: int, name: str, wattage: float):
        super().__init__(smart_home, db_conn, comp_id, name)
        self.wattage = wattage
