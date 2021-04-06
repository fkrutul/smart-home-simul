import logging

class Thermostat(object):

    def __init__(self, smart_home, HVAC, set_temp: float=70.0, temp_range: float=2.0) -> None:
        self.smart_home = smart_home
        self.HVAC = HVAC
        self.set_temp = set_temp
        self.temp_range = temp_range
        self.mode = None

    def check_temp(self):
        in_engage_range = (self.set_temp-self.temp_range) < self.smart_home.int_temp < (self.set_temp+self.temp_range)
        in_disengage_range = (self.set_temp-0.1) < self.smart_home.int_temp < (self.set_temp+0.1)
        if self.HVAC.engaged and in_disengage_range:
            self.HVAC.disengage()
            self.mode = None
        elif self.HVAC.engaged and self.mode == "heat" and self.set_temp <= self.smart_home.int_temp:
            self.HVAC.disengage()
            self.mode = None
        elif self.HVAC.engaged and self.mode == "cool" and self.set_temp >= self.smart_home.int_temp:
            self.HVAC.disengage()
            self.mode = None
        if not self.HVAC.engaged and not in_engage_range:
            self.HVAC.engage()
            if self.set_temp > self.smart_home.int_temp:
                self.mode = "heat"
            else:
                self.mode = "cool"
