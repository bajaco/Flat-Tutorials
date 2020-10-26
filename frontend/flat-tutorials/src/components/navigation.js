import React from 'react';
import { LinkContainer } from 'react-router-bootstrap';
import Nav from 'react-bootstrap/Nav'
import Navbar from 'react-bootstrap/Navbar';
class Navigation extends React.Component {
  render () {
    return (
      <Navbar variant='light'> 
        <Nav variant='dark'>
          <Nav.Item>
            <LinkContainer to='/'>
              <Nav.Link>Home</Nav.Link>
            </LinkContainer>
          </Nav.Item> 
          <Nav.Item>
            <LinkContainer to='/users'>
              <Nav.Link>Users</Nav.Link>
            </LinkContainer>
          </Nav.Item> 
          <Nav.Item>
            <LinkContainer to='/tutorial1'>
              <Nav.Link>Tutorial 1</Nav.Link>
            </LinkContainer>
          </Nav.Item>
        </Nav>
      </Navbar>
      
    );
  }
}
export default Navigation
