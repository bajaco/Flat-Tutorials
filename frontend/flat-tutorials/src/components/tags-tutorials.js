import React, { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom';
import { useAuth0 } from '@auth0/auth0-react';
import Badge from 'react-bootstrap/Badge';

const TagsTutorials = () =>{
  const [ tutorials, setTutorials ] = useState()
  const { tagname } = useParams();
  useEffect(() => {
    (async () => {
      try {
        
        const response = await fetch('http://localhost:5000/published/tags/' + tagname);
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
export default TagsTutorials
