import React, {useEffect, Component} from 'react';
//import TutorialsList from './components/tutorials-list';
import Header from './components/header';
import Nav from './components/nav.js';
import Users from './components/users.js';
import SignupButton from './components/signup-button.js';
import Profile from './components/profile.js';
import { Auth0Provider } from '@auth0/auth0-react';


class App extends Component {

  state = {
    users: []
  }
  /*
  componentDidMount() {
    fetch('http://localhost:5000/published')
    .then(res => res.json())
    .then((data) => {
      this.setState({ tutorials: data['tutorials']})
    })
    .catch(console.log)
  }
  */

  render() {
    return (
      <Auth0Provider
        domain='agyx.auth0.com'
        clientId='btQeJ55ezH0ejA6JSDTTzeTR5NZ4fv5b'
        responseType='token id_token'
        redirectUri={window.location.origin}
        audience='http://localhost:5000/'
        scope='openid email profile list:users'
        
        
      >
        <React.Fragment>
          <Header />
          <SignupButton />
          <Nav />
          <Users />
          
        </React.Fragment>
      </Auth0Provider>
    )
  }
}

export default App;


