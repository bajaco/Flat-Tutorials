import React, { useEffect, useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react';
import { Redirect } from 'react-router-dom';
import Card from 'react-bootstrap/Card';

const Users = () => {
  const { getAccessTokenSilently } = useAuth0();
  const [ users, setUsers ] = useState();
  const [ authError, setAuthError] = useState();
  useEffect(() => {
    (async () => {
      try {
        const token = await getAccessTokenSilently({
          audience: process.env.REACT_APP_AUDIENCE,
          scope: 'list:users',
        });
        const response = await fetch(process.env.REACT_APP_API_URL + '/admin/users', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setUsers(await response.json());
      } catch(e) {
        setAuthError(true);
      }
    })();
  }, [getAccessTokenSilently]);
   

  if (authError) {
    return(
      <Redirect to='/' />
    );
  }

  if (users) {
    if (!users['success']){
      return (<h3>Unauthorized</h3>)
    }
    return (
      <div> 
      {users['users'].map((user) => (
        <Card>
          <Card.Header>
            { user.username }
          </Card.Header>
          <ul>
            <li>id: {user['id']}</li>
            <li>auth0_id: {user['auth0_id']}</li>
            <li>email: {user['email']}</li>
            <li>published: {user['published']}</li>
          </ul>
        </Card>
      ))}
      </div>
    );
    
  } else {
    return (
      <div class="spinner-border" role="status">
        <span class="sr-only">Loading...</span>
      </div>
    );
  }
};
 


export default Users;
