import React, { Component } from 'react';

import {Button, Form} from 'react-bootstrap';


class ControlPanel extends Component {
    constructor(props) {
        super(props); 
        this.state = {
            lang_map: {
                control_weather: {
                    "en": "Control Weather:",
                    "fr": "Contrôler la Météo:"
                },
                set_ext_temp: {
                    "en": "Set Ext. Temp:",
                    "fr": "Régler la Temp Ext.:"
                },
                temp_delta: {
                    "en": "Temp. Delta:",
                    "fr": "Delta de Temp.:"
                },
                water_to_heat: {
                    "en": "Water to heat:",
                    "fr": "De L'eau à Chauffer:"
                },
                current_wattage: {
                    "en": "Current Wattage:",
                    "fr": "Puissance Actuelle:"
                },
                simulation_speed: {
                    "en": "Simulation Speed:",
                    "fr": "Vitesse de Simulation:"
                },
                up: {
                    "en": "Up",
                    "fr": "Haut"
                },
                down: {
                    "en": "Down",
                    "fr": "Bas"
                },
                reset: {
                    "en": "Reset",
                    "fr": "Remettre"
                },
                current: {
                    "en": "Current",
                    "fr": "Actuel"
                },
                clear: {
                    "en": "Clear",
                    "fr": "Clair"
                },
                clouds: {
                    "en": "Cloudy",
                    "fr": "Nuageux"
                },
                rain: {
                    "en": "Rainy",
                    "fr": "Pluvieux"
                },
                snow: {
                    "en": "Snowy",
                    "fr": "Neigeux"
                },
                thunderstorm: {
                    "en": "Stormy",
                    "fr": "Orageux"
                },
            },
        }
    }

    getWeatherDropdown() {
        return (
            <Form.Control
                as="select"
                custom
                onChange={this.props.setWeather}
            >
                <option value="Current">{this.state.lang_map.current[this.props.lang]}</option>
                <option value="Clear">{this.state.lang_map.clear[this.props.lang]}</option>
                <option value="Clouds">{this.state.lang_map.clouds[this.props.lang]}</option>
                <option value="Rain">{this.state.lang_map.rain[this.props.lang]}</option>
                <option value="Snow">{this.state.lang_map.snow[this.props.lang]}</option>
                <option value="Thunderstorm">{this.state.lang_map.thunderstorm[this.props.lang]}</option>
            </Form.Control>
        );
    }

    getSimSpeedDropdown() {
        return (
            <Form.Control
                as="select"
                custom
                onChange={this.props.setSpeed}
            >
                <option value="1">1x</option>
                <option value="2">2x</option>
                <option value="3">3x</option>
                <option value="5">5x</option>
            </Form.Control>
        );
    }

    getExtTempControl() {
        return (
            <div className="ext-temp-cont">
                <Button variant="secondary" className="temp-up" onClick={this.props.extTempIncrease}>{this.state.lang_map.up[this.props.lang]}</Button>
                <Button variant="secondary" className="temp-down" onClick={this.props.extTempDecrease}>{this.state.lang_map.down[this.props.lang]}</Button>
                <Button variant="secondary" className="reset" onClick={this.props.resetTemp}>{this.state.lang_map.reset[this.props.lang]}</Button>
            </div>
        );
    }


    render() {
        return (
            <div className="control-panel">
                <h3 className="weather-cont-title">{this.state.lang_map.control_weather[this.props.lang]}</h3>
                <div className="weather-cont">{this.getWeatherDropdown()}</div>
                <h3 className="ext-temp-cont-title">{this.state.lang_map.set_ext_temp[this.props.lang]}</h3>
                {this.getExtTempControl()}
                <h3 className="temp-delta-title">{this.state.lang_map.temp_delta[this.props.lang]}</h3>
                <h3 className="temp-delta">{this.props.temp_delta}&#176;F/sec.</h3>
                <h3 className="water-title">{this.state.lang_map.water_to_heat[this.props.lang]}</h3>
                <h3 className="water">{this.props.water_to_heat} gallons</h3>
                <h3 className="wattage-title">{this.state.lang_map.current_wattage[this.props.lang]}</h3>
                <h3 className="wattage">{this.props.wattage} watts</h3>
                <h3 className="speed-title">{this.state.lang_map.simulation_speed[this.props.lang]}</h3>
                <div className="speed">{this.getSimSpeedDropdown()}</div>
            </div>
        );
    }

}

export default ControlPanel