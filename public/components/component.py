import logging

class Component(object):

    def __init__(self, smart_home, db_conn, comp_id: int, name: str) -> None:
        self.smart_home = smart_home
        self.db_conn = db_conn
        self.comp_id = comp_id
        self.name = name
