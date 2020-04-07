import React from 'react';
import Button from '@material-ui/core/Button';
import { Grid } from '@material-ui/core';
import Paper from '@material-ui/core/Paper';
import { withStyles } from '@material-ui/core/styles';
import InputAdornment from "@material-ui/core/InputAdornment";
import People from "@material-ui/icons/People";
import Icon from "@material-ui/core/Icon";
import LockIcon from '@material-ui/icons/Lock';
import NavBar from './NavBar';
import axios from 'axios';
import BackgroundSlideshow from 'react-background-slideshow'
import LoginButton from './LoginButton'

import logo from "../images/logo.png";
import place from "../images/placeholder.png"
import alentejo from "../images/alentejo.jpg"
import casas from "../images/casas.jpg"
import coastline from "../images/coastline.jpg"
import plains from "../images/plains.jpg"
import hillside from "../images/hillside.jpg"
import sintra from "../images/sintra.jpeg"





const styles = theme => ({
    root: {
        backgroundImage: logo,
    },
    loginButton: {
        fontFamily: 'Karla, sans-serif',
        color: '#2268B2',
        border: 'solid',
        borderColor: '#8B8982',
        backgroundColor: "#f5f5f5",
        fontSize: '1em',
        paddingTop: '1vh',
        paddingBottom: '1vh',
        marginBottom: '15vh',
        textAlign: 'center'
    },
    background: {
        height: 1356,
        background: "../images/logo.png"
    },
    iconPaper: {
        height: '30vh', // responsive height is 30vh, 180px
        borderStyle: 'solid',
        borderColor: '#8B8982',
        marginTop: '20vh',
        marginBottom: '5vh',
        borderRadius: '15px'
        
    },
    welcomePaper: {
        fontFamily: 'Karla, sans-serif',
        width: '26vw',
        borderStyle: 'solid',
        backgroundColor: "#f5f5f5",
        color: "#2268B2",
        borderColor: '#8B8982',
        paddingRight: '5vw',
        paddingLeft: '5vw',
        textAlign: 'center',
        marginTop: '5vh',
        marginBottom: '2vh',
    },
    inputPaper: {
        border: 'solid',
        borderColor: '#59bf8e',
        color: '#3e8563',
        fontFamily: 'Karla, sans-serif',
        paddingRight: '3vw',
        paddingLeft: '3vw',
        paddingBottom: '3vh',
        marginBottom: '3vh',
        width: '40vw'
    },
    searchField: {
        color: '#3e8563',
        fontFamily: 'Karla, sans-serif',
    },
    searchFieldLabel: {
        color: '#3e8563',
        fontFamily: 'Karla, sans-serif',
    },
    searchUnderline: {
        color: 'red !important'
    }

})



export default withStyles(styles)(class LoginPage extends React.Component {

    state = {
        username: undefined,
        password: undefined,
        isClicked: false,
        data: undefined,
        background: plains
    };

    BackgroundHead = {
        backgroundImage: null,
        height: '100vh',
        backgroundSize: 'cover'
        }

    componentDidMount() {

        const rand = Math.floor(Math.random() * 4);
        console.log(rand);
        if (rand == 0) {
            this.setState({background: hillside});
        }
        else if (rand == 1) {
            this.setState({background: sintra});
        }
        else if (rand == 2) {
            this.setState({background: coastline});
        }
        else if (rand == 3) {
            this.setState({background: plains});
        }
    }

    render() {
        
        const {classes} = this.props;
        return (
            <div style={{backgroundImage: 'url('+ this.state.background +')',height: '100vh',backgroundSize: 'cover'}}>
                <Grid
                    container
                    spacing={0}
                    direction="column"
                    alignItems="center"
                    justify="center"
                >
                    <div>
                    <img className={classes.iconPaper} src={logo} />
                  </div>
                    <Paper color="primary" className={classes.welcomePaper}>
                        <div><h1>Welcome to idioma!</h1></div>
                    </Paper>

                    
                    
                    <Grid item xs={3} >
                        <LoginButton/>
                    </Grid>
                </Grid>
            </div>
        )
    }
})