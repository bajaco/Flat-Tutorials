import React, { useEffect, useState } from 'react'
import { useAuth0 } from '@auth0/auth0-react';

const Users = () => {
  const { getAccessTokenSilently } = useAuth0();
  const [ users, setUsers ] = useState()
  
  useEffect(() => {
    (async () => {
      try {
        const token = await getAccessTokenSilently({
          audience: 'http://localhost:5000/',
          scope: 'list:users',
        });
        const response = await fetch('http://localhost:5000/admin/users', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setUsers(await response.json());
      } catch(e) {
        console.error(e);
      }
    })();
  }, [getAccessTokenSilently]);
  
  if (users) {
 
    return (
      <div> 
      {users['users'].map((user) => (
        <h1>{ user.username }</h1>
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
