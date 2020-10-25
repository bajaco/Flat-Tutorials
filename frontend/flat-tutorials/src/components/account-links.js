import React from "react";
import { useAuth0 } from "@auth0/auth0-react";

const AccountLinks = () => {
  const { loginWithRedirect, logout, isAuthenticated } = useAuth0();
  
  if (!isAuthenticated) {
    return (
      <div id="account-links">
        <button
          className="btn btn-primary btn-block"
          onClick={() =>
            loginWithRedirect({
              screen_hint: "login",
            })
          }
        >
          Login/Signup
        </button>
      </div>
    );
  }

  return (
    <div id="account-links">
      <button
        className="btn btn-primary btn-block"
        onClick={() =>
          logout({
            screen_hint: "logout",
          })
        }
      >
        Logout
      </button>
    </div>
  );


};

export default AccountLinks;
