import React from 'react';
import { Redirect } from 'react-router-dom';
import PublicMenu from './public-menu.js';
import AdminMenu from './admin-menu.js';
import ModMenu from './mod-menu.js';
import RegisteredMenu from './registered-menu.js';
import { useAuth0 } from '@auth0/auth0-react';

const Navigation = () => {
  const { user } = useAuth0();
  
  if (!user) {
    return (<PublicMenu />);
  } else {
    if (user[process.env.REACT_APP_ROLES_URL].includes('administrator')) {
      return (<AdminMenu />);
    } else if (user[process.env.REACT_APP_ROLES_URL].includes('moderator')) {
      return (<ModMenu />);
    } else if (user[process.env.REACT_APP_ROLES_URL].includes('registered_user')) {
      return (<RegisteredMenu />);
    } else {
      return (<Redirect to='/' />);
    }
  }
}
export default Navigation
