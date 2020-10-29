import React, { useEffect, useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react';
import Badge from 'react-bootstrap/Badge';
import { Link } from 'react-router-dom';

const UserList = () => {
  const { getAccessTokenSilently } = useAuth0();
  const [ tutorials, setTutorials ] = useState()

  useEffect(() => {
    (async () => {
      try {
        const token = await getAccessTokenSilently({
          audience: process.env.REACT_APP_AUDIENCE,
          scope: 'submit:tutorial',
        });

        const response = await fetch(process.env.REACT_APP_API_URL + '/submitted', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setTutorials(await response.json());
      } catch(e) {
        console.error(e);
      }
    })();
  }, [getAccessTokenSilently]);

  if (!tutorials) {
    return (
      <div class="spinner-border" role="status">
        <span class="sr-only">Loading...</span>
      </div>
    )
  } else if (!tutorials['success']) {
    return(
      <h3>No tutorials found!</h3>
    );
  } else {
    return (
      <div id="tutorials-list"> 
        {tutorials['tutorials'].map((tutorial) => (
          <div class="card mb-sm-2">
            <div class="card-header">
              {tutorial['under_review'] &&
                <Badge variant="warning">
                  Under Review
                </Badge>
              }
              {tutorial['published'] &&
                  <Badge variant="success">
                    Published
                  </Badge>
              }
              {!tutorial['under_review'] && !tutorial['published'] &&
                  <Badge variant="danger">
                    Rejected
                  </Badge>
              }
            </div>
            <div class="card-body d-flex flex-row justify-content-between">
              <Link class='text-dark' to={'/my-tutorials/' + tutorial.id}>
                <h5 class="card-title">{tutorial.title}</h5>
              </Link>
                           
            </div>
            <div class='card-footer d-flex flex-row justify-content-between'>
              <div>
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
              <i>by {tutorial.author}  </i>
            </div>
          </div>
        ))}
      </div>
    );
  }
}
export default UserList;
