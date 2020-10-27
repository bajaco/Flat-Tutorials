import React from 'react';

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
    if (user['http://localhost:3000/roles'].includes('administrator')) {
      return (<AdminMenu />);
    } else if (user['http://localhost:3000/roles'].includes('moderator')) {
      return (<ModMenu />);
    } else if (user['http://localhost:3000/roles'].includes('registered_user')) {
      return (<RegisteredMenu />);
    }
  }
}
export default Navigation
