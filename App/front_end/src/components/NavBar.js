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


const NavBar = () => {
  const { isAuthenticated, loginWithRedirect, logout } = useAuth0();
  //const {classes} = this.props;
  console.log(isAuthenticated);

  return (
    <div >
        {isAuthenticated && <Paper elevation={10} style={{position: 'fixed', width: '100vw', zIndex: 10000}} square>
            <Grid container alignItems="center" >
                <Grid container item xs={12} sm={3} justify="center">
                    <img style={{marginTop: '2vh', marginBottom: '2vh', width: '300px'}} src={logo} />
                </Grid>
                <Grid container xs={12} sm={9} item justify="space-around" >
                    <Grid item>
                        <NavLink to="/dash" style={{ textDecoration: 'none'}}><Button style={{marginTop: '2vh',marginBottom: '2vh',width: '15vw',borderStyle: 'solid',color: '#2268B2',border: 'solid',borderColor: '#9CBDD2',backgroundColor: "#f5f5f5", fontSize: '1em',}} variant="contained" >Learning Center</Button></NavLink>
                    </Grid>
                    <Grid item>
                        <NavLink to="/mydocs" style={{ textDecoration: 'none'}}><Button style={{marginTop: '2vh',marginBottom: '2vh',width: '15vw',borderStyle: 'solid',color: '#2268B2',border: 'solid',borderColor: '#9CBDD2',backgroundColor: "#f5f5f5", fontSize: '1em',}} variant="contained" >My Documents</Button></NavLink>
                    </Grid>
                    <Grid item>
                        <NavLink to="/achievements" style={{ textDecoration: 'none'}}><Button style={{marginTop: '2vh',marginBottom: '2vh',width: '15vw',borderStyle: 'solid',color: '#2268B2',border: 'solid',borderColor: '#9CBDD2',backgroundColor: "#f5f5f5", fontSize: '1em',}} variant="contained" >Achievements</Button></NavLink>
                    </Grid>
                    <Grid item>
                        <Button style={{marginTop: '2vh',marginBottom: '2vh',width: '15vw',borderStyle: 'solid',color: '#2268B2',border: 'solid',borderColor: '#9CBDD2',backgroundColor: "#f5f5f5", fontSize: '1em',}} variant="contained"  onClick={() => logout()}>Log out!</Button>
                    </Grid>
                </Grid>
            </Grid>
        </Paper>}
    </div>
  );
};

export default NavBar;