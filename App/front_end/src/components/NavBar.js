import React from 'react';
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
        fontFamily: 'Karla, sans-serif',
        borderStyle: 'solid',
        
        fontFamily: 'Karla, sans-serif',
        color: '#2268B2',
        border: 'solid',
        borderColor: '#8B8982',
        backgroundColor: "#f5f5f5",
        fontSize: '1em',
    }
})

export default withStyles(styles)(class NavHeader extends React.Component {
    render() {
        const {classes} = this.props;
        console.log(this.props.auth.isAuthenticated());
        
        if (window.location.pathname === '/') return null;
        {
            return (
            <Paper square><header>{this.props.auth.isAuthenticated() &&
                <Grid container alignItems="center" >
                    <Grid container item xs={12} sm={3} justify="center">
                        <img className={classes.logo} src={logo} />
                    </Grid>
                    <Grid container xs={12} sm={9} item justify="space-around" >
                        <Grid item>
                            <NavLink to="/dash" style={{ textDecoration: 'none'}}><Button className={classes.headerButton} variant="contained" >Learning Center</Button></NavLink>
                        </Grid>
                        <Grid item>
                            <Button className={classes.headerButton} variant="contained" >My Documents</Button>
                        </Grid>
                        <Grid item>
                            <Button className={classes.headerButton} variant="contained" >Achievements</Button>
                        </Grid>
                        <Grid item>
                            <Button className={classes.headerButton} variant="contained"  onClick={this.props.handleSubmit}>Logout</Button>
                        </Grid>
                    </Grid>
                </Grid>
        }</header></Paper>
        );
        }
    }
})