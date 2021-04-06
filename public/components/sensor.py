from .component import Component
import logging


class Sensor(Component):

    def __init__(self, smart_home, db_conn, comp_id: str, name: str):
        super().__init__(smart_home, db_conn, comp_id, name)
        self.engaged = False
    
    def engage(self):
        if not self.engaged:
            self.engaged = True
            if not self.smart_home.debug:
                self.db_conn.logStartEvent(self.comp_id, self.smart_home.current_time)
            else:
                logging.info(f"{self.smart_home.current_time}: {self.name} engaged!")

    def disengage(self):
        if self.engaged:
            self.engaged = False
            if not self.smart_home.debug:
                self.db_conn.logEndEvent(self.comp_id, self.smart_home.current_time)
            else:
                logging.info(f"{self.smart_home.current_time}: {self.name} disengaged!")
