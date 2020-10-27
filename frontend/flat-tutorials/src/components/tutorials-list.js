import React, { useEffect, useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react';
import Badge from 'react-bootstrap/Badge';
import { Link } from 'react-router-dom';

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
        <div class="card mb-sm-2">
          <div class="card-body d-flex flex-row justify-content-between">
            <Link class='text-dark' to={'/tutorials/' + tutorial.id}>
              <h5 class="card-title">{tutorial.title}</h5>
            </Link>
            <i>by {tutorial.author}  </i>
          </div>
          <div class='card-footer'>
            {tutorial['tags'].map((tag) => (       
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
        </div>
      ))}
    </div>
  );
  
}
export default TutorialsList
