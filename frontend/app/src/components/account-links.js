import React from "react";
import Button from 'react-bootstrap/Button';
import { useAuth0 } from "@auth0/auth0-react";

const AccountLinks = () => {
  const { loginWithRedirect, logout, isAuthenticated } = useAuth0();
  
  if (!isAuthenticated) {
    return (
      <div id="account-links">
        <Button
          variant='outline-dark'
          onClick={() =>
            loginWithRedirect({
              screen_hint: "login",
            })
          }
        >
          Login/Signup
        </Button>
      </div>
    );
  }

  return (
    <div id="account-links">
      <Button
        variant='outline-dark' 
        onClick={() =>
          logout({
            screen_hint: "logout",
          })
        }
      >
        Logout
      </Button>
    </div>
  );


};

export default AccountLinks;
