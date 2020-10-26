import React from 'react';
import AccountLinks from './account-links.js';
import Navigation from './navigation.js';
class Header extends React.Component {

  render () {
    return (
      <div class='header d-flex flex-row justify-content-between align-items-center'>
        <h1>flat tutorials</h1>
        <Navigation />
        <AccountLinks />
      </div>
    );
  }
}
export default Header
