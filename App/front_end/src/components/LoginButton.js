import React from "react";
import { useAuth0 } from "../react-auth0-spa";
import Paper from '@material-ui/core/Paper';

import Grid from '@material-ui/core/Grid';
import { NavLink } from 'react-router-dom';
import logo from '../images/logo.png'
import Button from '@material-ui/core/Button';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';

const styles = theme => ({
    logo: {
        marginTop: '2vh',
        marginBottom: '2vh',
        width: '300px'
    },
    headerButton: {
        marginTop: '2vh',
        marginBottom: '2vh',
        width: '15vw',
        borderStyle: 'solid',
        color: '#2268B2',
        border: 'solid',
        borderColor: '#9CBDD2',
        backgroundColor: "#f5f5f5",
        fontSize: '1em',
    }
})


const LoginButton = () => {
  const { isAuthenticated, loginWithRedirect, logout } = useAuth0();
  //const {classes} = this.props;
  console.log(isAuthenticated);

  return (
    <div>
        {!isAuthenticated && <Button style={{marginTop: '2vh',marginBottom: '2vh',width: '15vw',borderStyle: 'solid',color: '#2268B2',border: 'solid',borderColor: '#9CBDD2',backgroundColor: "#f5f5f5", fontSize: '1em',}} variant="contained"  onClick={() => loginWithRedirect()}>Log in!</Button>}
    </div>
  );
};

export default LoginButton;