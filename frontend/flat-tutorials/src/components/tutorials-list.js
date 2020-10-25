import React, { useEffect, useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react';

const TutorialsList = () => {
  const { getAccessTokenSilently } = useAuth0();
  const [ tutorials, setTutorials ] = useState()

  useEffect(() => {
    (async () => {
      try {
        const response = await fetch('http://localhost:5000/published');
        setTutorials(await response.json());
      } catch(e) {
        console.error(e);
      }
    })();
  }, []);

  if (!tutorials) {
    return (
      <div>
        <h1>loading . . .</h1>
      </div>
    )
  }

  return (
    <div id="tutorials-list"> 
      {tutorials['tutorials'].map((tutorial) => (
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
export default TutorialsList
