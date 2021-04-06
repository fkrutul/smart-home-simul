import React, { Component } from 'react';
import io from "socket.io-client";

import {Modal, Button, Form} from 'react-bootstrap';

import PersonnelTable from "./PersonnelTable";


const ENDPOPINT = "http://localhost:5000";


class Personnel extends Component {
    constructor() {
        super();
        this.state = {
            response: [],
            showModal: false,
            firstName: "",
            lastName: "",
            position: "",
            phone: ""
        };
        // this.addPerson = this.addPerson.bind(this);
        this.deletePerson = this.deletePerson.bind(this);
        this.editPerson = this.editPerson.bind(this);
        this.closeModal = this.closeModal.bind(this);
        this.handleFirstName = this.handleFirstName.bind(this);
        this.handleLastName = this.handleLastName.bind(this);
        this.handlePosition = this.handlePosition.bind(this);
        this.handlePhone = this.handlePhone.bind(this);
    }

    closeModal() {
      this.setState({showModal: false});
      this.setState({firstName: ""});
      this.setState({lastName: ""});
      this.setState({position: ""});
      this.setState({phone: ""});
    }

    handleFirstName(e) {
      this.setState({firstName: e.target.value});
    }

    handleLastName(e) {
      this.setState({lastName: e.target.value});
    }

    handlePosition(e) {
      this.setState({position: e.target.value});
    }

    handlePhone(e) {
      this.setState({phone: e.target.value});
    }

    changeState = data => {
      this.setState({ response: data });
    };
    
    componentDidMount() {
        this.socket = io.connect(ENDPOPINT, {rejectUnauthorized: false});
        console.log("connected", this.socket);
        this.socket.on("send_personnel", this.changeState);
        this.socket.emit("send_personnel");
    }

    componentWillUnmount() {
        this.socket.off("send_personnel");
        this.socket.disconnect();
        console.log("disconnected", this.socket);
    }

    deletePerson = (personId) => {
        console.log(personId)
        this.socket.emit("delete_person", personId)
    }

    editPerson = (newValue, personId, column) => {
      // console.log(column)
      this.socket.emit("edit_person", {"newValue": newValue, "personId": personId, "column": column})
  }

    addPerson = (e) => {
      e.preventDefault();
      this.socket.emit("add_person", {
        "firstName": this.state.firstName,
        "lastName": this.state.lastName,
        "position": this.state.position,
        "phone": this.state.phone
      });
      this.closeModal()
    }

    render() {
      return (
        <div>
            <Button 
              variant="success"
              onClick={() => this.setState({showModal: true})}>Add Personnel
            </Button>
            <Modal show={this.state.showModal} onHide={this.closeModal}>
              <Modal.Header closeButton>
                <Modal.Title>Add Personnel</Modal.Title>
              </Modal.Header>
              <Modal.Body>
                <Form onSubmit={this.addPerson}>
                  <Form.Label>First Name</Form.Label>
                  <Form.Control 
                    type="text"
                    placeholder="First Name"
                    value={this.state.firstName}
                    onChange={this.handleFirstName}
                  />
                  <Form.Label>Last Name</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="Last Name"
                    value={this.state.lastName}
                    onChange={this.handleLastName} 
                  />
                  <Form.Label>Position</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="Position"
                    value={this.state.position}
                    onChange={this.handlePosition}
                  />
                  <Form.Label>Phone Number</Form.Label>
                  <Form.Control
                    type="text"
                    placeholder="Phone Number"
                    value={this.state.phone}
                    onChange={this.handlePhone}
                  />
                  <Button type="submit">
                    Submit
                  </Button>
                </Form>
              </Modal.Body>
            </Modal>
            <PersonnelTable
              personData={this.state.response}
              deletePerson={this.deletePerson}
              editPerson={this.editPerson}
            />
        </div>
      );
    }
  }

export default Personnel;