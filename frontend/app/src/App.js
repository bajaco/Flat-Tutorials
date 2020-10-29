
import React, {Component} from 'react';
import { BrowserRouter as Router,
  Switch, Route } from 'react-router-dom';
import Header from './components/header';
import Users from './components/users.js';
import TutorialsList from './components/tutorials-list.js';
import PublicTutorial from './components/public-tutorial.js';
import TagsTutorials from './components/tags-tutorials.js';
import UserList from './components/user-list.js';
import UserTutorial from './components/user-tutorial.js';
import Create from './components/create.js';
import ReviewList from './components/review-list.js';
import ReviewTutorial from './components/review-tutorial.js';
import { Auth0Provider } from '@auth0/auth0-react';
import Container from 'react-bootstrap/Container';


class App extends Component {
  render() {
    return (
      <Router>
        <Auth0Provider
          domain={process.env.REACT_APP_DOMAIN}
          clientId={process.env.REACT_APP_CLIENT_ID}
          responseType={process.env.REACT_APP_RESPONSE_TYPE}
          redirectUri={window.location.origin}
          audience={process.env.REACT_APP_AUDIENCE}
          scope={process.env.REACT_APP_SCOPE}
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
              <Route path='/my-tutorials/:tutorialid' children={<UserTutorial />} />
              <Route path='/my-tutorials'>
                <UserList />
              </Route>
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


