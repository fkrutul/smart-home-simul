import json

from meteostat import Stations, Hourly
from datetime import datetime, timedelta


def create_datetime_ID(dt):
    out = ""
    out += str(dt.year) + str(dt.month).zfill(2) + str(dt.day).zfill(2)
    out += str(dt.hour).zfill(2) + str(dt.minute).zfill(2)
    return out


def interpolate_minutes(row1, row2):
    out = {}
    current_time = row1.time - timedelta(hours=6)
    current_temp = row1.temp
    out[create_datetime_ID(current_time)] = {"time": current_time, "temp": current_temp}
    gap = (row2.temp - row1.temp)/60 
    for _ in range(59):
        current_time += timedelta(minutes=1)
        current_temp += gap
        out[create_datetime_ID(current_time)] = {"time": current_time, "temp": current_temp}
    return out


def fetch(
    start=datetime(2020, 1, 1),
    end=datetime.now(),
    lat=33.5020, # Closest to UAB
    lon=-86.8064):
    start += timedelta(hours=6)  # UTC offset
    end += timedelta(hours=6)
    end.replace(microsecond=0, second=0)
    stations = Stations(lat=lat, lon=lon)
    station = stations.fetch(1)
    data = Hourly(station, start, end)
    data = data.normalize()
    data = data.interpolate()
    df = data.fetch()
    out = {}
    last_row = None
    for row in df.itertuples():
        if last_row:
            out.update(interpolate_minutes(last_row, row))
        last_row = row
    current_time = last_row.time - timedelta(hours=6)
    while current_time <= end - timedelta(hours=6):
        out[create_datetime_ID(current_time)] = {"time": current_time, "temp": last_row.temp}
        current_time += timedelta(minutes=1)
    return out
