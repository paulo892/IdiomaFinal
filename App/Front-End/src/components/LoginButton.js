import React from "react";
import { useAuth0 } from "../react-auth0-spa";
import Button from '@material-ui/core/Button';

// component for a button allowing a user to log into the application
const LoginButton = () => {
  
  // constants used in authentication
  const { isAuthenticated, loginWithRedirect } = useAuth0();

  return (
    <div>
        {!isAuthenticated && <Button style={{marginTop: '2vh',marginBottom: '2vh',width: '15vw',borderStyle: 'solid',color: '#2268B2',border: 'solid',borderColor: '#9CBDD2',backgroundColor: "#f5f5f5", fontSize: '1em',}} variant="contained"  onClick={() => loginWithRedirect()}>Log in!</Button>}
    </div>
  );
};

export default LoginButton;