import React, {Component} from 'react';
import { BrowserRouter as Router,
  Switch, Route, Link } from 'react-router-dom';
import Header from './components/header';
import Users from './components/users.js';
import TutorialsList from './components/tutorials-list.js';
import PublicTutorial from './components/public-tutorial.js';
import TagsTutorials from './components/tags-tutorials.js';
import Create from './components/create.js';
import ReviewList from './components/review-list.js';
import ReviewTutorial from './components/review-tutorial.js';
import { Auth0Provider } from '@auth0/auth0-react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';

class App extends Component {

  render() {
    return (
      <Router>
        <Auth0Provider
          domain='agyx.auth0.com'
          clientId='btQeJ55ezH0ejA6JSDTTzeTR5NZ4fv5b'
          responseType='token id_token'
          redirectUri={window.location.origin}
          audience='http://localhost:5000/'
          scope='openid email profile list:users submit:tutorial view:unpublished_list view:unpublished'
        >
          <Container>
            <link
              rel="stylesheet"
              href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"
              integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk"
              crossorigin="anonymous"
            />  
            <Header />
            <Switch>
              <Route path="/tags/:tagname" children={<TagsTutorials />} />
              <Route path='/tutorials/:tutorialid' children={<PublicTutorial />} />
              <Route path='/review/:tutorialid' children={<ReviewTutorial />} />
              <Route path='/users'>
                <Users />
              </Route>
              <Route path='/review'>
                <ReviewList />
              </Route>
              <Route path='/create'>
                <Create />
              </Route>
              <Route path='/'>
                <TutorialsList />
              </Route>
            </Switch>
          </Container>
        </Auth0Provider>
      </Router>
    )
  }
}

export default App;


