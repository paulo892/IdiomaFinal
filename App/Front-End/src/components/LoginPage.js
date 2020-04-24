import React from 'react';
import { Grid } from '@material-ui/core';
import Paper from '@material-ui/core/Paper';
import { withStyles } from '@material-ui/core/styles';
import LoginButton from './LoginButton'
import logo from "../images/logo.png";
import coastline from "../images/coastline.jpg"
import plains from "../images/plains.jpg"
import hillside from "../images/hillside.jpg"
import sintra from "../images/sintra.jpeg"

// component styles
const styles = theme => ({
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
        height: '30vh',
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
    }
})

// component that welcomes the user and allows them to log in
export default withStyles(styles)(class LoginPage extends React.Component {

    state = {
        username: undefined, // user's username
        password: undefined, // user's password
        background: plains // selected background
    };

    // details describing the page background
    BackgroundHead = {
        backgroundImage: null,
        height: '100vh',
        backgroundSize: 'cover'
    }

    // after mount, sets the page background at random!
    componentDidMount() {
        const rand = Math.floor(Math.random() * 4);
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