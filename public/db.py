import psycopg2
from datetime import timedelta
from .smarthome_builder import build_home
from .calculate import *

class DBWriter(object):
    def __init__(self):
        self.conn = psycopg2.connect(database = "Team1DB", user = "Team1", password = "1Team1", host = "164.111.161.243", port = "5432")
        self.activeEvents = {} #Events that have not finished {id : [beginTime]}
        self.pastEvents = {}  #Events that have finished {id : [(start1, end1), (start2, end2)]...}
        self.power_usage = 0
        self.water_usage = 0
        self.cost = 0
        self.monthly_power = 0
        self.monthly_water = 0
        self.monthly_cost = 0
        self.monthly_usage = {}
        self.daily_usage = {}
        self.day_counter = 0
        self.health ={'date_' : '', 'faye_temps' : '', 'ed_temps' : '', 'spike_temps' : '', 'jet_temps' : ''}
        self.i = 0
        self.writable =[]
        self.wattages = self.initWattages()
        print("Opened database successfully")

    def initWattages(self):
        wattages = {}
        keys = ["appliances", "lights"]
        items = build_home(0)
        for key in keys:
            for item in items[key]:
                wattages[item[1]] = item[3]
        return wattages


    def logStartEvent(self, id, st_time):
        self.activeEvents[id] = [st_time]

    def logEndEvent(self, id, end_time, wattage=0):
        times = self.activeEvents.pop(id)
        times.append(end_time)
        times.append(wattage)
        pastTimes = self.pastEvents.get(id, [])
        pastTimes.append(tuple(times))
        self.pastEvents[id] = pastTimes
        if len(self.pastEvents) >= 10:
            self.writeToDB()

    def calculateUsage(self):
        writable = []
        for k,v in self.pastEvents.items():
            wattage = self.wattages.get(k, 0)
            if k.find('-') != -1:
                m = k.split('-')
                k = m[0] + m[1]
            for i in v:
                duration = i[1] - i[0]
                duration = duration.total_seconds()
                self.power_usage += wattage * duration
                if k.find('bath') != -1:
                    if duration == 1200:   #bath
                        self.water_usage += 30
                    else:
                        self.water_usage += 25
                if k.find('diswasher') != -1:
                    self.water_usage += 6
                if k.find('clotheswasher') != -1:
                    self.water_usage += 20
                writable.append((k, i[0].isoformat(), i[1].isoformat(), duration))
        self.pastEvents.clear()
        return writable

    def writeToDB(self):
        ##writes events to db
        inserts = self.calculateUsage()
        for insert in inserts:
            com = f'INSERT INTO {insert[0]} (begin_time, end_time, duration) VALUES (\'{insert[1]}\', \'{insert[2]}\',{insert[3]})'
            with self.conn.cursor() as curs:
                curs.execute(com)
        self.conn.commit()

    def writeDailyUsage(self, today):
        ##writes daily usage to db and adds to monthly usage
        watt_seconds_to_KWH = 3600000
        power_KWH = self.power_usage/watt_seconds_to_KWH
        self.cost = electricityCost(power_per_second(self.power_usage)) + waterCost(self.water_usage)
        with self.conn.cursor() as curs:
            curs.execute(f'INSERT INTO daily_usage(date_, power, water, cost) VALUES (\'{today}\', {power_KWH}, {self.water_usage}, {self.cost})')
            self.conn.commit()
        self.monthly_water += self.water_usage
        self.monthly_power += self.power_usage
        self.monthly_cost += self.cost
        self.daily_usage[self.day_counter] = {'power' : self.power_usage, 'water' : self.water_usage}
        self.power_usage = 0
        self.water_usage = 0
        self.cost = 0
        self.day_counter += 1
        if self.day_counter == 30 or self.day_counter == 60 or self.day_counter == 90:
            self.monthly_usage[self.i] = {'power' : self.monthly_power/watt_seconds_to_KWH, 'water' : self.monthly_water, 'cost' :self.monthly_cost}
            with self.conn.cursor() as curs:
                curs.execute(f'INSERT INTO monthly_usage(month, power, water, cost) VALUES ({self.i}, {self.monthly_power/watt_seconds_to_KWH}, {self.monthly_water}, {self.monthly_cost})')
                curs.execute('SELECT * FROM public.reset()')
                curs.fetchall()
                self.conn.commit()
            self.monthly_power = 0
            self.monthly_water = 0
            self.monthly_cost = 0
            self.i += 1

    def writeTemp(self, name, temp, today):
        ##writes the temperature logs
        if self.health['date_'] == '':
            self.health['date_'] = today
        self.health[name.lower() + '_temps'] = temp
        if self.health['date_'] != '' and self.health['faye_temps'] != '' and self.health['ed_temps'] != '' and self.health['spike_temps'] != '' and self.health['jet_temps'] != '':
            with self.conn.cursor() as curs:
                com = f'INSERT INTO health(date_, faye_temps, ed_temps, spike_temps, jet_temps) VALUES (\'{self.health["date_"]}\', {self.health["faye_temps"]}, {self.health["ed_temps"]}, {self.health["spike_temps"]}, {self.health["jet_temps"]})'
                curs.execute(com)
                self.conn.commit()
                self.health ={'date_' : '', 'faye_temps' : '', 'ed_temps' : '', 'spike_temps' : '', 'jet_temps' : ''}

    def doProjection(self, today):
        ##does 30 day future projection
        proj_power = 0
        proj_water = 0
        for i in range(31):
            month1_power = self.daily_usage[i]['power']
            month2_power = self.daily_usage[i+30]['power']
            month1_water = self.daily_usage[i]['water']
            month2_water = self.daily_usage[i+30]['water']
            proj_power = (month1_power + month2_power)/2
            proj_water = (month1_water + month2_water)/2
            self.power_usage = proj_power
            self.water_usage = proj_water
            today = today + timedelta(days = 1)
            self.writeDailyUsage(today)