import React, { useEffect, useState } from 'react';
import { useAuth0 } from '@auth0/auth0-react';
import { Link, useParams } from 'react-router-dom';
import Badge from 'react-bootstrap/Badge';

const PublicTutorial = () => {
 
  const [ tutorial, setTutorial ] = useState()
  const { tutorialid } = useParams();
  useEffect(() => {
    (async () => {
      try {
        const response = await fetch('http://localhost:5000/published/' + tutorialid);
        setTutorial(await response.json());
      } catch(e) {
        console.error(e);
      }
    })();
  }, [tutorialid]);

  if (!tutorial) {
    return (
      <div>
        <h1>loading . . .</h1>
      </div>
    )
  } else if (!tutorial['success']) {
    return (
      <h3>Not found.</h3>
    );
  }

  return (
    <div class='tutorial'>  
      <div class='tutorial-header'>
        <h3>{ tutorial['tutorial']['title'] }</h3>
        {tutorial['tutorial']['tags'].map((tag) => (
          <>
            <Link to={'/tags/' + tag}>
              <Badge variant='dark'>
                {tag}
              </Badge>
            </Link>
          {' '}
          </>
          
        ))}
      </div> 
      <p>{tutorial['tutorial']['text']}</p>
    </div>
  );
  
}
export default PublicTutorial
