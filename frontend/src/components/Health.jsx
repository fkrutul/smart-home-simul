import io from "socket.io-client";
import React, { Component } from 'react';
import { Line } from 'react-chartjs-2';

const ENDPOPINT = "http://localhost:5000";

class Health extends Component {
  constructor() {
    super();
    this.state = {
        response: {},
        labels : [],
        datasets: []
    };
}

getData = data => {
  this.setState({ response: data });
  console.log(data);
    var dates = [],
    faye_temps_ = [],
    ed_temps_ = [],
    spike_temps_ = [],
    jet_temps_ = [];
  data.sort(function(a, b) {return (a['date_'] > b['date_'])? 1 : -1});
  data.forEach(date_ =>{dates.push(date_.date_)})
  data.forEach(faye_temps =>{faye_temps_.push(faye_temps.faye_temps)})
  data.forEach(ed_temps =>{ed_temps_.push(ed_temps.ed_temps)})
  data.forEach(spike_temps =>{spike_temps_.push(spike_temps.spike_temps)})
  data.forEach(jet_temps =>{jet_temps_.push(jet_temps.jet_temps)})
  this.setState({response: data,
                 labels : dates, 
                 datasets: [
                  {
                    label : 'Faye Temps',
                    fill: false,
                    lineTension: 0.75,
                    backgroundColor: 'rgb(227, 91, 91, 0.5)',
                    borderColor: 'rgb(227, 91, 91, 0.8)',
                    borderWidth: 2,
                    data : faye_temps_
                  },
                  {
                  label : 'Ed Temps',
                  fill: false,
                  lineTension: 0.75,
                  backgroundColor: 'rgb(0, 102, 204, 0.5)',
                  borderColor: 'rgb(0, 102, 204, 0.8)',
                  borderWidth: 2,
                  data : ed_temps_
                  },
                  {
                    label : 'Spike Temps',
                    fill: false,
                    lineTension: 0.75,
                    backgroundColor: 'rgb(58, 95, 11, 0.5)',
                    borderColor: 'rgb(58, 95, 11, 0.8)',
                    borderWidth: 2,
                    data : spike_temps_
                    },
                    {
                      label : 'Jet Temps',
                      fill: false,
                      lineTension: 0.75,
                      backgroundColor: 'rgb(61, 72, 73, 0.5)',
                      borderColor: 'rgb(61, 72, 73, 0.8)',
                      borderWidth: 2,
                      data : jet_temps_
                      }
                ]});
}

componentDidMount() {
  this.socket = io.connect(ENDPOPINT, {rejectUnauthorized: false});
  console.log("connected", this.socket);
  this.socket.on("health_data", this.getData);
  this.socket.emit('health_data')
}

componentWillUnmount() {
  this.socket.off("health_data");
  this.socket.disconnect();
  console.log("disconnected", this.socket);
}
    render() {
      return (
        <div>
            <Line
             data={this.state}
             options = {{
               title:{
                 dispalay : true,
                 text : 'Temperature Data',
                 fontsize:20
               },
            legend : {
              display:true,
              position : 'right'
            }
          }
        }
        />
        </div>
      );
    }
  }

export default Health;