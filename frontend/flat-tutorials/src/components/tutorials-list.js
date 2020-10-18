import React from 'react'
class TutorialsList extends React.Component {
  render () {
    return (
      <div> 
        {this.props.tutorials.map((tutorial) => (
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">{tutorial.title}</h5>
              <h7><i>submitted by {tutorial.author}</i></h7>
              <p><b>{tutorial.tags.join(', ')}</b></p>
            </div>
          </div>
        ))}
      </div>
    );
  }
}
export default TutorialsList
