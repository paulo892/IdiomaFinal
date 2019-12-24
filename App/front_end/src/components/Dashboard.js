import React from 'react';
import Button from '@material-ui/core/Button';
import { Grid } from '@material-ui/core';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Paper from '@material-ui/core/Paper';
import { withStyles } from '@material-ui/core/styles';
import InputAdornment from "@material-ui/core/InputAdornment";
import People from "@material-ui/icons/People";
import Icon from "@material-ui/core/Icon";
import LockIcon from '@material-ui/icons/Lock';
import axios from 'axios';

import logo from "../images/logo.png";


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
    },
    mainPaper: {
        marginTop: '5vh',
        color: '#8B8982',
        fontFamily: 'Karla, sans-serif',
        paddingRight: '3vw',
        paddingLeft: '3vw',
        paddingBottom: '3vh',
        marginBottom: '3vh',
        width: '60vw'
    }

})



export default withStyles(styles)(class LoginPage extends React.Component {

    state = {
        username: undefined,
        password: undefined,
        isClicked: false,
        data: undefined
    };

    getUsers = async () => {
        await axios.get(
            '/api/getUsers',
            {
                headers: {'Content-type': 'application/json'}
            }
        ).then((data) => {
            let details = data['data'];
            details.map((n) => {
                const full_name = n.firstname + " " + n.lastname;
                n['fullname'] = full_name;
            });
            this.setState({data: data['data']});
        })}

    handleUsernameChange = (e) => {
        this.setState({username: e.target.value});
        console.log(e.target.value);
    }

    handlePasswordChange = (e) => {
        this.setState({password: e.target.value});
        // <img className={classes.icon} src={logo} />
    }

    handleSubmit = (e) => {
        //this.getUsers();
        this.props.submitBehavior();
    }

    render() {
        
        const {classes} = this.props;
        return (
            <div>
                <Grid
                    container
                    spacing={0}
                    direction="column"
                    alignItems="center"
                    justify="center"
                >
                
                    <Paper square className={classes.mainPaper}>
                        <div style={{textAlign: 'center'}}><h1>What have you been working on recently?</h1></div>
                    </Paper>

                    <Paper className={classes.mainPaper}>
                        <Grid
                            container
                            alignItems="center"
                            justify="center"
                        >
                            <Grid item>
                                <ExpansionPanel>
                                    <ExpansionPanelSummary>
                                        Beginner
                                    </ExpansionPanelSummary>
                                    <ExpansionPanelDetails>
                                        Beginner stuff
                                    </ExpansionPanelDetails>
                                </ExpansionPanel>
                            </Grid>
                            <Grid item>
                            </Grid>
                            <Grid item>
                            </Grid>
                        
                        </Grid>
                    </Paper>




                    

                    
                    
                    <Grid item xs={3} >
                        <Button className={classes.loginButton} variant="contained"  onClick={this.handleSubmit}>Log out with Auth0!</Button>
                    </Grid>
                </Grid>
            </div>
        )
    }
})