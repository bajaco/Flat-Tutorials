import React from 'react';
import { LinkContainer } from 'react-router-bootstrap';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

const PublicMenu = () => {
  
  return (
    <Navbar variant='light'> 
      <Nav variant='dark'>
        <Nav.Item>
          <LinkContainer to='/'>
            <Nav.Link>Home</Nav.Link>
          </LinkContainer>
        </Nav.Item> 
      </Nav>
    </Navbar>
      
    );
}
export default PublicMenu;
