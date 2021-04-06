import React, { Component } from 'react';

import {Button} from 'react-bootstrap';

import {ReactComponent as ThunderIcon} from "../icons/static/thunder.svg";
import {ReactComponent as CloudyIcon} from "../icons/static/cloudy.svg";
import {ReactComponent as RainyIcon} from "../icons/static/rainy-6.svg";
import {ReactComponent as ClearIcon} from "../icons/static/day.svg";
import {ReactComponent as SnowyIcon} from "../icons/static/snowy-6.svg";
import {ReactComponent as WeatherIcon} from "../icons/static/weather.svg";



class Dashboard extends Component {
    constructor(props) {
        super(props);
        this.state = {
            lang_map: {
                current_time: {
                    "en": "Current Time:",
                    "fr": "Heure Actuelle:"
                },
                interior_temp: {
                    "en": "Interior Temp:",
                    "fr": "Température Intérieure:"
                },
                up: {
                    "en": "Up",
                    "fr": "Haut"
                },
                set_temp: {
                    "en": "Set temperature:",
                    "fr": "Température Actuelle:"
                },
                down: {
                    "en": "Down",
                    "fr": "Bas"
                },
                ext_temp: {
                    "en": "Exterior temperature:",
                    "fr": "Température Extérieure:"
                }
            },
        }
    }

    

    getWeatherIcon() {
        var weather = this.props.weather_main;
        if(weather == "Clear") {
            return <ClearIcon />
        } else if (weather == "Clouds") {
            return <CloudyIcon />
        } else if (weather == "Rain" || weather == "Drizzle") {
            return <RainyIcon />
        } else if (weather == "Snow") {
            return <SnowyIcon />
        } else if (weather == "Thunderstorm") {
            return <ThunderIcon />
        } else {
            return <WeatherIcon />
        }
    }

    render() {
        return (
            <div className="dashboard-container">
                <h3 className="time">{this.state.lang_map.current_time[this.props.lang]}<br />{this.props.current_time}</h3>
                <h3 className="date">{this.props.current_date}</h3>
                <h3 className="int-temp">{this.state.lang_map.interior_temp[this.props.lang]}<br />{this.props.int_temp}&#176;F</h3>
                <Button variant="secondary" className="temp-up" onClick={this.props.setTempIncrease}>{this.state.lang_map.up[this.props.lang]}</Button>
                <h3 className="set-temp">{this.state.lang_map.set_temp[this.props.lang]}<br />{this.props.set_temp}&#176;F</h3>
                <Button variant="secondary" className="temp-down" onClick={this.props.setTempDecrease}>{this.state.lang_map.down[this.props.lang]}</Button>
                <h3 className="ext-temp">{this.state.lang_map.ext_temp[this.props.lang]}<br />{this.props.ext_temp}&#176;F</h3>
                <h3 className="weather">{this.props.weather_main}<br />{this.props.weather_desc}</h3>
                <div className="weather-icon">{this.getWeatherIcon()}</div>
            </div>
        );
    }

}

export default Dashboard