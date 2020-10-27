import React from 'react';
import { LinkContainer } from 'react-router-bootstrap';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

const RegisteredMenu = () => {
  
  return (
    <Navbar variant='light'> 
      <Nav variant='dark'>
        <Nav.Item>
          <LinkContainer to='/'>
            <Nav.Link>Home</Nav.Link>
          </LinkContainer>
        </Nav.Item> 
        <Nav.Item>
          <LinkContainer to='/create'>
            <Nav.Link>Create</Nav.Link>
          </LinkContainer>
        </Nav.Item> 
        <Nav.Item>
          <LinkContainer to='/my-tutorials'>
            <Nav.Link>My Tutorials</Nav.Link>
          </LinkContainer>
        </Nav.Item> 
      </Nav>
    </Navbar>
      
    );
}
export default RegisteredMenu;
