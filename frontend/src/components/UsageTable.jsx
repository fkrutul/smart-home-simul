import React, { Component } from 'react';
import BootstrapTable from 'react-bootstrap-table-next';
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';


class UsageTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
            columns: [
                {
                    dataField: "month",
                    text: "Month",
                },
                {
                    dataField: "power",
                    text: "Power",
                },
                {
                    dataField: "water",
                    text: "Water",
                },
                {
                    dataField: "cost",
                    text: "Cost",
                }
            ]
        };
    }


    render() {
        return (
            <BootstrapTable 
                keyField="month"
                data={this.props.props}
                columns={this.state.columns}
            />
        );
    }

}

export default UsageTable