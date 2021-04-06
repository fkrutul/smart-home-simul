import React, { Component } from 'react';
import io from "socket.io-client";

import Dashboard from "./Dashboard";

import ImageMapper from "react-image-mapper";

import houseLayout from "../house_layout.jpeg";

const ENDPOPINT = "http://localhost:5000";


const ENGAGED_COLOR = "rgba(40, 230, 20, 0.5)";
const DISENGAGED_COLOR = "rgba(196, 20, 20, 0.5)";
var AREAS_MAP = {
    name: "components",
    areas: [
        {name: "light_01", shape: "rect", coords: [800, 265, 845, 310], preFillColor: DISENGAGED_COLOR,},
        {name: "light_02", shape: "rect", coords: [100, 255, 143, 300], preFillColor: DISENGAGED_COLOR,},
        {name: "light_03", shape: "rect", coords: [95, 581, 138, 625], preFillColor: DISENGAGED_COLOR,},
        {name: "light_04", shape: "rect", coords: [735, 322, 774, 359], preFillColor: DISENGAGED_COLOR,},
        {name: "light_05", shape: "rect", coords: [860, 323, 898, 360], preFillColor: DISENGAGED_COLOR,},
        {name: "light_06", shape: "rect", coords: [48, 213, 87, 250], preFillColor: DISENGAGED_COLOR,},
        {name: "light_07", shape: "rect", coords: [170, 215, 209, 252], preFillColor: DISENGAGED_COLOR,},
        {name: "light_08", shape: "rect", coords: [45, 650, 83, 687], preFillColor: DISENGAGED_COLOR,},
        {name: "light_09", shape: "rect", coords: [45, 525, 82, 562], preFillColor: DISENGAGED_COLOR,},
        {name: "light_10", shape: "rect", coords: [844, 449, 889, 493], preFillColor: DISENGAGED_COLOR,},
        {name: "light_11", shape: "rect", coords: [113, 465, 158, 510], preFillColor: DISENGAGED_COLOR,},
        {name: "light_12", shape: "rect", coords: [335, 298, 378, 343], preFillColor: DISENGAGED_COLOR,},
        {name: "light_13", shape: "rect", coords: [270, 225, 309, 264], preFillColor: DISENGAGED_COLOR,},
        {name: "light_14", shape: "rect", coords: [270, 370, 310, 410], preFillColor: DISENGAGED_COLOR,},
        {name: "light_15", shape: "rect", coords: [725, 82, 770, 127], preFillColor: DISENGAGED_COLOR,},
        {name: "tv_01", shape: "rect", coords: [800, 178, 856, 230], preFillColor: DISENGAGED_COLOR,},
        {name: "tv_02", shape: "rect", coords: [230, 290, 285, 346], preFillColor: DISENGAGED_COLOR,},
        {name: "fan_01", shape: "rect", coords: [858, 508, 906, 556], preFillColor: DISENGAGED_COLOR,},
        {name: "fan_02", shape: "rect", coords: [113, 416, 157, 460], preFillColor: DISENGAGED_COLOR,},
        {name: "hvac_01", shape: "rect", coords: [451, 53, 526, 129], preFillColor: DISENGAGED_COLOR,},
        {name: "ref_01", shape: "rect", coords: [533, 105, 573, 152], preFillColor: DISENGAGED_COLOR,},
        {name: "water-heater_01", shape: "circle", coords: [629, 500, 21], preFillColor: DISENGAGED_COLOR,},
        {name: "microwave_01", shape: "rect", coords: [734, 49, 777, 77], preFillColor: DISENGAGED_COLOR,},
        {name: "stove_01", shape: "rect", coords: [626, 49, 685, 83], preFillColor: DISENGAGED_COLOR,},
        {name: "oven_01", shape: "rect", coords: [626, 83, 685, 90], preFillColor: DISENGAGED_COLOR,},
        {name: "dishwasher_01", shape: "rect", coords: [678, 125, 713, 160], preFillColor: DISENGAGED_COLOR,},
        {name: "clothes-washer_01", shape: "rect", coords: [559, 480, 599, 520], preFillColor: DISENGAGED_COLOR,},
        {name: "clothes-dryer_01", shape: "rect", coords: [559, 524, 599, 564], preFillColor: DISENGAGED_COLOR,},
        {name: "bath_01", shape: "rect", coords: [773, 524, 845, 565], preFillColor: DISENGAGED_COLOR,},
        {name: "bath_02", shape: "rect", coords: [39, 383, 72, 440], preFillColor: DISENGAGED_COLOR,},
        {name: "door_01", shape: "rect", coords: [314, 659, 366, 700], preFillColor: DISENGAGED_COLOR,},
        {name: "door_02", shape: "rect", coords: [778, 75, 821, 128], preFillColor: DISENGAGED_COLOR,},
        {name: "door_03", shape: "rect", coords: [502, 622, 542, 674], preFillColor: DISENGAGED_COLOR,},
        {name: "garage_01", shape: "rect", coords: [524, 798, 700, 807], preFillColor: DISENGAGED_COLOR,},
        {name: "garage_02", shape: "rect", coords: [735, 798, 911, 807], preFillColor: DISENGAGED_COLOR,},
        {name: "window_01", shape: "rect", coords: [918, 212, 928, 255], preFillColor: DISENGAGED_COLOR,},
        {name: "window_02", shape: "rect", coords: [918, 336, 928, 380], preFillColor: DISENGAGED_COLOR,},
        {name: "window_03", shape: "rect", coords: [77, 194, 122, 203], preFillColor: DISENGAGED_COLOR,},
        {name: "window_04", shape: "rect", coords: [30, 246, 40, 292], preFillColor: DISENGAGED_COLOR,},
        {name: "window_05", shape: "rect", coords: [96, 694, 140, 702], preFillColor: DISENGAGED_COLOR,},
        {name: "window_06", shape: "rect", coords: [30, 578, 40, 622], preFillColor: DISENGAGED_COLOR,},
        {name: "window_07", shape: "rect", coords: [918, 517, 928, 560], preFillColor: DISENGAGED_COLOR,},
        {name: "window_08", shape: "rect", coords: [30, 439, 40, 483], preFillColor: DISENGAGED_COLOR,},
        {name: "window_09", shape: "rect", coords: [263, 194, 309, 204], preFillColor: DISENGAGED_COLOR,},
        {name: "window_10", shape: "rect", coords: [350, 194, 395, 204], preFillColor: DISENGAGED_COLOR,},
        {name: "window_11", shape: "rect", coords: [437, 194, 482, 204], preFillColor: DISENGAGED_COLOR,},
        {name: "window_12", shape: "rect", coords: [580, 39, 625, 49], preFillColor: DISENGAGED_COLOR,},
        {name: "window_13", shape: "rect", coords: [682, 39, 726, 49], preFillColor: DISENGAGED_COLOR,},
    ]
};

class Layout extends Component {
    constructor() {
        super();
        this.state = {
            response: {
                "current_time": "...",
                "current_date": "...",
                "set_temp": "...",
                "int_temp": "...",
                "ext_temp": "...",
                "weather_main": "...",
                "weather_desc": "..."
            },
        };
        this.setTempIncrease = this.setTempIncrease.bind(this);
        this.setTempDecrease = this.setTempDecrease.bind(this);
    }

    updateState = data => {
        this.setState({ response: data });
        for(var i=0; i<AREAS_MAP.areas.length; i++) {
            var comp = AREAS_MAP.areas[i];
            if(this.state.response["components"][comp.name]) {
                AREAS_MAP.areas[i].preFillColor = ENGAGED_COLOR;
            }
            else {
                AREAS_MAP.areas[i].preFillColor = DISENGAGED_COLOR;
            }
        }
        this.setState({ response: data });
    }

    changeState = data => { this.setState({ response: data }) };
    
    componentDidMount() {
        this.socket = io.connect(ENDPOPINT, {rejectUnauthorized: false});
        console.log("connected", this.socket);
        this.socket.emit("init", {"page": "layout"});
        this.socket.on("send_state", this.updateState);
        this.socket.on("update_state", this.changeState);
        const handleRefresh = this.refresh.bind(this);
        setInterval(handleRefresh, 1000);
    }

    componentWillUnmount() {
        this.socket.off("send_state");
        this.socket.off("update_state");
        this.socket.disconnect();
        console.log("disconnected", this.socket);
    }

    refresh() {
        this.socket.emit("refresh", {"page": "layout"});
    }

    click_comp(area) {
        var comp_id = area.name;
        console.log(comp_id);
        if(comp_id.startsWith("light_") || comp_id.startsWith("garage_") || comp_id.startsWith("tv_") || comp_id.startsWith("door_")) {
            if(this.state.response["components"][comp_id]) {
                this.socket.emit("update_comp", {"comp_id": comp_id, "engaged": false, "page": "layout"})
            }
            else {
                this.socket.emit("update_comp", {"comp_id": comp_id, "engaged": true, "page": "layout"})
            }
        }
    }

    setTempIncrease() {
        this.socket.emit("change_set_temp", {"direction": "up", "page": "layout"})
    }

    setTempDecrease() {
        this.socket.emit("change_set_temp", {"direction": "down", "page": "layout"})
    }

    render() {
      return (
        <div>
            <div className="layout-container">
                <Dashboard 
                    current_time={this.state.response["current_time"]}
                    current_date={this.state.response["current_date"]}
                    set_temp={this.state.response["set_temp"]}
                    ext_temp={this.state.response["ext_temp"]}
                    int_temp={this.state.response["int_temp"]}
                    weather_main={this.state.response["weather_main"]}
                    weather_desc={this.state.response["weather_desc"]}
                    setTempIncrease={this.setTempIncrease}
                    setTempDecrease={this.setTempDecrease}
                    lang={this.props.lang}
                />
                <div className="floorplan">
                    <ImageMapper 
                        src={houseLayout}
                        map={AREAS_MAP}
                        width={1000}
                        onClick={area => this.click_comp(area)} 
                    />
                </div>
            </div>
        </div>
      );
    }
  }

export default Layout;
