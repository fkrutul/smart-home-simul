from datetime import datetime, timedelta
import json

# pip
from flask import Flask
from flask_socketio import SocketIO, emit, send
from pyowm.owm import OWM
from psycopg2.extras import RealDictCursor

from .smart_home import SmartHome
from .local_config import API_key
from .simulation import Simulation
from .components import Appliance

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
SH = SmartHome()
ADMIN_SH = SmartHome(debug=True)
SIM = Simulation(SH)
ADMIN_SIM = Simulation(ADMIN_SH)
#SIM.simulate(timedelta(days=60))  # Uncomment this to do data generation before sim


def get_state(page):
    sim = SIM
    if page == "admin":
        sim = ADMIN_SIM
    state = {}
    time = sim.smart_home.current_time
    weekday_map = {
        0: "Mon.",
        1: "Tue.",
        2: "Wed.",
        3: "Thu.",
        4: "Fri.",
        5: "Sat.",
        6: "Sun."
    }
    state["current_time"] = time.strftime("%H:%M:%S")
    state["current_date"] = weekday_map[time.weekday()] + " " + time.strftime("%b. %d, %Y")
    state["int_temp"] = round(sim.smart_home.int_temp, 2)
    state["set_temp"] = sim.smart_home.thermostat.set_temp
    state["ext_temp"] = round(sim.current_temp, 2)
    state["weather_main"] = sim.weather_main
    state["weather_desc"] = sim.weather_desc
    state["components"] = {}
    state["temp_delta"] = round(sim.temp_delta, 5)
    state["water_to_heat"] = round(sim.water_to_heat, 2)
    state["wattage"] = 0
    for k, v in sim.smart_home.components.items():
        state["components"][k] = v.engaged
        if type(v) == Appliance and v.engaged:
            state["wattage"] += v.wattage
    return state


@socketio.on("init")
def connect_socket(data):
    sim = SIM
    if data["page"] == "admin":
        sim = ADMIN_SIM
    print("CONNECTED TO CLIENT!!!!")
    sim.init_sim_state()
    emit("send_state", get_state(data["page"]))

@socketio.on("refresh")
def refresh(data):
    sim = SIM
    if data["page"] == "admin":
        sim = ADMIN_SIM
    sim.increment_time()
    emit("send_state", get_state(data["page"]))

@socketio.on("update_comp")
def update_set_temp(data):
    sim = SIM
    if data["page"] == "admin":
        sim = ADMIN_SIM
    engaged = data["engaged"]
    comp_id = data["comp_id"]
    if engaged:
        print("Engaging " + comp_id)
        sim.smart_home.components[comp_id].engage()
        comp_pre = comp_id.split("_")[0]
        if comp_pre == "bath":
            sim.water_to_heat += (30*.65)
        elif comp_pre == "dishwasher":
            sim.water_to_heat += 6
        elif comp_pre == "clothes-washer":
            sim.water_to_heat += (20*.85)
    else:
        print("Disengaging " + comp_id)
        sim.smart_home.components[comp_id].disengage()
    emit("send_state", get_state(data["page"]))

@socketio.on("change_set_temp")
def change_set_temp(data):
    sim = SIM
    if data["page"] == "admin":
        sim = ADMIN_SIM
    if data["direction"] == "up":
        sim.smart_home.thermostat.set_temp += 1
        sim.smart_home.thermostat.check_temp()
    else:
        sim.smart_home.thermostat.set_temp -= 1
        sim.smart_home.thermostat.check_temp()
    emit("send_state", get_state(data["page"]))

@socketio.on("change_ext_temp")
def change_ext_temp(data):
    sim = SIM
    if data["page"] == "admin":
        sim = ADMIN_SIM
    if data["direction"] == "up":
        sim.current_temp += 1
        sim.debug_temp = True
        sim.smart_home.thermostat.check_temp()
    else:
        sim.current_temp -= 1
        sim.debug_temp = True
        sim.smart_home.thermostat.check_temp()
    emit("send_state", get_state(data["page"]))

@socketio.on("reset_temp")
def reset_temp(data):
    sim = SIM
    if data["page"] == "admin":
        sim = ADMIN_SIM
    sim.current_temp += 1
    sim.debug_temp = False
    sim.update_weather()
    sim.smart_home.thermostat.check_temp()
    emit("send_state", get_state(data["page"]))

@socketio.on("set_weather")
def set_weather(data):
    sim = SIM
    if data["page"] == "admin":
        sim = ADMIN_SIM
    status = data["weather"]
    if status == "Current":
        sim.debug_weather = False
        sim.update_weather()
    else:
        sim.debug_weather = True
        sim.weather_main = status
        sim.weather_desc = "None"
    emit("send_state", get_state(data["page"]))

@socketio.on("set_speed")
def set_speed(data):
    speed = int(data["speed"])
    sim = SIM
    if data["page"] == "admin":
        sim = ADMIN_SIM
    sim.sim_speed = speed
    
@socketio.on('get_chart_data')
def get_usage_data():
    data = {'chart_data' : '',
            'table_data' : ''}
    con = SH.db_conn.conn
    with con.cursor() as curs:
        curs.execute('SELECT array_to_json(array_agg(row_to_json(daily_usage))) FROM daily_usage;')
        chart_data = curs.fetchall()
        data['chart_data'] = chart_data[0][0]
        curs.execute('SELECT array_to_json(array_agg(row_to_json(monthly_usage))) FROM monthly_usage;')
        table_data = curs.fetchall()
        data['table_data'] = table_data[0][0]
    emit("get_data", data)

@socketio.on('delete_person')
def delete_person(data):
    del_id = data
    conn = SH.db_conn.conn
    with conn.cursor() as curs:
        curs.execute('UPDATE public.personnel SET active = false WHERE id=%s', (del_id,))
    conn.commit()
    send_personnel()

@socketio.on('edit_person')
def edit_person(data):
    personId = data["personId"]
    newValue = data["newValue"]
    column = data["column"]["dataField"]
    conn = SH.db_conn.conn
    with conn.cursor() as curs:
        curs.execute(f"UPDATE public.personnel SET {column} = %s WHERE id=%s", (newValue, personId))
    conn.commit()
    send_personnel()

@socketio.on('add_person')
def add_person(data):
    firstName = data["firstName"]
    lastName = data["lastName"]
    position = data["position"]
    phone = data["phone"]
    conn = SH.db_conn.conn
    with conn.cursor() as curs:
        curs.execute('INSERT INTO public.personnel (first_name, last_name, position, phone, active) VALUES (%s, %s, %s, %s, %s)',
        (firstName, lastName, position, phone, True))
    conn.commit()
    send_personnel()
    

@socketio.on('send_personnel')
def send_personnel():
    conn = SH.db_conn.conn
    with conn.cursor(cursor_factory=RealDictCursor) as curs:
        curs.execute('SELECT * FROM public.personnel WHERE active = true')
        personnel = curs.fetchall()
    emit("send_personnel", personnel)

@socketio.on('health_data')
def health_data():
     conn = SH.db_conn.conn
     with conn.cursor() as curs:
        curs.execute('SELECT array_to_json(array_agg(row_to_json(health))) FROM health;')
        data = curs.fetchall()
        emit("health_data", data[0][0])

if __name__ == "__main__":
    socketio.run(app)
