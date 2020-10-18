import React, {Component} from 'react';
import TutorialsList from './components/tutorials-list';
import Header from './components/header';
import Nav from './components/nav.js';

class App extends Component {

  state = {
    tutorials: []
  }

  componentDidMount() {
    fetch('http://localhost:5000/published')
    .then(res => res.json())
    .then((data) => {
      this.setState({ tutorials: data['tutorials']})
    })
    .catch(console.log)
  }
  render() {
    return (
      <React.Fragment>
        <Header />
        <Nav />
        <TutorialsList tutorials={this.state.tutorials} />
      </React.Fragment>
    )
  }
}

export default App;


