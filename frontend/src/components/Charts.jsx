import React, { Component } from 'react';
import { Line } from 'react-chartjs-2';
import io from "socket.io-client";
import UsageTable from "./UsageTable";

const ENDPOPINT = "http://localhost:5000";

class Charts extends Component {
  constructor() {
    super();
    this.state = {
        response: {'chart_data': [],
                   'table_data' : []
                  },
        labels : [],
        datasets: [],
        table_data : []
    };
}

getData = data => {
  this.setState({ response: data });
  this.state.table_data = data['table_data'];
    var dates = [],
    power_ = [],
    water_ = [],
    cost_ = [];
  data['chart_data'].sort(function(a, b) {return (a['date_'] > b['date_'])? 1 : -1});
  data['chart_data'].forEach(date_ =>{dates.push(date_.date_)})
  data['chart_data'].forEach(power =>{power_.push(power.power)})
  data['chart_data'].forEach(water =>{water_.push(water.water)})
  data['chart_data'].forEach(cost =>{cost_.push(cost.cost)})
  this.setState({response: data,
                 labels : dates, 
                 datasets: [
                  {
                    label : 'Power Usage',
                    fill: false,
                    lineTension: 0.75,
                    backgroundColor: 'rgb(227, 91, 91, 0.5)',
                    borderColor: 'rgb(227, 91, 91, 0.8)',
                    borderWidth: 2,
                    data : power_
                  },
                  {
                  label : 'Water Usage',
                  fill: false,
                  lineTension: 0.75,
                  backgroundColor: 'rgb(0, 102, 204, 0.5)',
                  borderColor: 'rgb(0, 102, 204, 0.8)',
                  borderWidth: 2,
                  data : water_
                  },
                  {
                    label : 'Total Cost',
                    fill: false,
                    lineTension: 0.75,
                    backgroundColor: 'rgb(58, 95, 11, 0.5)',
                    borderColor: 'rgb(58, 95, 11, 0.8)',
                    borderWidth: 2,
                    data : cost_
                    }
                ]});
}

componentDidMount() {
  this.socket = io.connect(ENDPOPINT, {rejectUnauthorized: false});
  console.log("connected", this.socket);
  this.socket.on("get_data", this.getData);
  this.socket.emit('get_chart_data')
}

componentWillUnmount() {
  this.socket.off("get_data");
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
                 text : 'Monthly Usage Data',
                 fontsize:20
               },
            legend : {
              display:true,
              position : 'right'
            }
          }
        }
        />
        <UsageTable
        props = {this.state.table_data}
        />
        </div>
      );
    }
  }

export default Charts;