# STL
import os
import fnmatch
import json

# local
from public import SmartHome

# pip
from flask import (
    render_template,
    Blueprint,
    current_app,
    request,
    send_from_directory
)

BP = Blueprint("routes", __name__)
SH = SmartHome()


def get_state():
    state = {}
    state["int_temp"] = SH.int_temp
    state["ext_temp"] = SH.thermostat.set_temp
    state["components"] = {}
    for k, v in SH.components.items():
        state["components"][k] = v.engaged
    return state

@BP.route("/state")
def send_state():
    return {200: json.dumps(get_state())}


@BP.route("/update-comp")
def update_set_temp():
    update = request.get_json()
    engaged = update["engaged"]
    comp_id = update["comp_id"]
    if engaged:
        SH.components[comp_id].engage()
    elif not engaged:
        SH.components[comp_id].disengage()
    return {200: json.dumps(get_state())}

@BP.route('/get-data')
def get_usage_data():
    data = ''
    con = SH.db_conn.conn    #hopefully were already connected
    with con.cursor() as curs:
        curs.execute('SELECT array_to_json(array_agg(row_to_json(daily_usage))) FROM daily_usage;')
        data = curs.fatchall()
    return {200: json.dumps(data)}

@BP.route("/layout")
def get_layout():
    response = {200: "Layout Placeholder"}
    return response


@BP.route("/charts")
def get_charts():
    response = {200: "Charts Placeholder"}
    return response


@BP.route("/admin")
def get_admin():
    response = {200: "Admin Placeholder"}
    return response
