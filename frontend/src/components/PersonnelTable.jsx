import React, { Component } from 'react';

import {Button} from 'react-bootstrap';
import BootstrapTable from 'react-bootstrap-table-next';
import cellEditFactory from 'react-bootstrap-table2-editor';
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';


class PersonnelTable extends Component {
    constructor(props) {
        super(props);
        this.state = {
            columns: [
                {
                    dataField: "first_name",
                    text: "First Name",
                },
                {
                    dataField: "last_name",
                    text: "Last Name",
                    sort: true
                },
                {
                    dataField: "position",
                    text: "Position",
                },
                {
                    dataField: "phone",
                    text: "Phone #",
                },
                {
                    dataField: "id",
                    text: "Delete",
                    formatter: (row) => {
                        return (
                            <Button
                                onClick={() => {this.props.deletePerson(row)}}
                            >
                                Delete
                            </Button>
                        );
                    },
                }
            ]
        };
    }


    render() {
        return (
            <BootstrapTable 
                keyField="id"
                data={this.props.personData}
                columns={this.state.columns}
                defaultSorted={
                    [{
                        dataField: "last_name",
                        order: "asc"
                    }]
                }
                cellEdit={cellEditFactory({
                    mode: "click",
                    afterSaveCell: (oldValue, newValue, row, column) => {
                        this.props.editPerson(newValue, row.id, column);
                    }
                })}
            />
        );
    }

}

export default PersonnelTable