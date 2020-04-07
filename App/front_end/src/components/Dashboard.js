import React from 'react';
import Button from '@material-ui/core/Button';
import { Grid } from '@material-ui/core';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Paper from '@material-ui/core/Paper';
import { withStyles } from '@material-ui/core/styles';
import InputAdornment from "@material-ui/core/InputAdornment";
import People from "@material-ui/icons/People";
import Icon from "@material-ui/core/Icon";
import LockIcon from '@material-ui/icons/Lock';
import Checkbox from '@material-ui/core/Checkbox';
import axios from 'axios';
import FormGroup from '@material-ui/core/FormGroup';
import {Link} from "react-router-dom";
import FormControlLabel from '@material-ui/core/FormControlLabel';
import { NavLink } from 'react-router-dom';
import DocumentPage from './DocumentPage'

import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';

import logo from "../images/logo.png";


const styles = theme => ({
    root: {
        backgroundImage: logo,
    },
    loginButton: {
        color: '#2268B2',
        border: 'solid',
        borderColor: '#9CBDD2',
        backgroundColor: "#f5f5f5",
        fontSize: '1em',
        paddingTop: '1vh',
        paddingBottom: '1vh',
        marginBottom: '15vh',
        marginTop: '5vh',
        textAlign: 'center'
    },
    loginButtonDisabled: {
        color: '#2268B2',
        border: 'solid',
        borderColor: '#9CBDD2',
        backgroundColor: "#f5f5f5",
        fontSize: '1em',
        paddingTop: '1vh',
        paddingBottom: '1vh',
        marginBottom: '15vh',
        marginTop: '5vh',
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
    questionPaper: {
        marginTop: '30vh',
        color: '#2268B2',
        fontFamily: 'Karla, sans-serif',
        paddingTop: '1vw',
        paddingRight: '3vw',
        borderColor: '#2268B2',
        paddingLeft: '3vw',
        backgroundColor: '#f5f5f5',
        paddingBottom: '3vh',
        marginBottom: '10vh',
        width: '50vw'
    },
    expansionPanel: {
        backgroundColor: '#f5f5f5',
        marginBottom: '5vh',
        color: '#2268B2',
        width: '25vw'
    },
    backgroundDiv: {
        backgroundColor: '#58ABDE',
        height: '100vh',
        width: '100vw'
    }
})





export default withStyles(styles)(class LoginPage extends React.Component {

    // TODO - Better sort these topics
    beginner_topics = ['Números', 'Preposições', 'Superlativos', 'Interrogativos', "Presente Indicativo (Regular)", "Presente Indicativo (Irregular)", "Ser vs. Estar"];
    intermediate_topics = ["Pretérito Indicativo (Regular)", "Pretérito Indicativo (Irregular)", "Imperfeito (Regular)", "Imperfeito (Irregular)","Presente Gerúndio","Presente Subjuntivo (Regular)","Presente Indicativo (Irregular)"];
    advanced_topics = ["Passado Subjuntivo (Regular)","Passado Subjuntivo (Irregular)","Presente Perfeito","Pretérito Perfeito","Futúro Indicativo (Regular)","Futúro Indicativo (Irregular)","Futúro Perfeito","Condicional (Regular)","Condicional (Irregular)"];

    state = {
        attributes: [],
        experience: [],
        articleId: null,
        articlePrepared: false
    }

    componentWillMount() {
        axios.get(
            '/api/getUserExperience',
            {
                params: {
                    email: this.props.email
                }
                
            },
            {
                headers: {'Content-type': 'application/json'}
            }
        ).then((data) => {
            const result = data['data'];
            console.log(result);
            this.setState({experience: result});
        })
    }

    

    getArticleId = async() => {
        await axios.get(
            '/api/getArticleId',
            {
                params: {
                    attributes: this.state.attributes,
                    email: this.props.email
                }
                
            },
            {
                headers: {'Content-type': 'application/json'}
            }
        ).then((data) => {
            let details = data['data'];
            console.log(details);

            window.alert('Article ' + details + ' prepared! Ready to continue.' );

            if (details != 'a') {
                this.setState({articlePrepared: true, articleId: details})
            }
        })
        
    }
    onClick = (e) => {
        let checked = e.target.checked;
        let val = e.target.value;
        let vals = this.state.attributes;

        if (checked) {
            vals.push(val);
            this.setState(() => ({
                attributes: vals
            }), console.log(this.state.attributes))
        }
        else {
            let i = this.state.attributes.indexOf(val);
            if (i > -1) {
                vals.splice(i, 1);
                this.setState(() => ({
                    attributes: vals
                }), console.log(this.state.attributes))
            }
        }
        
    }

    render() {

        console.log(this.props.email);

        const {classes} = this.props;
        return (
            <div className={classes.backgroundDiv}>
                <Grid
                    container
                    spacing={0}
                    direction="column"
                    alignItems="center"
                    justify="center"
                >
                
                    <Paper rounded elevation={10} className={classes.questionPaper}>
                        <div style={{textAlign: 'center'}}><h1>What have you been working on recently?</h1></div>
                    </Paper>

                    <Grid
                        container
                        alignItems="center"
                        justify="center"
                        spacing={7}
                    >
                        <Grid item styles={{marginRight: '2vw', marginLeft: '2vw'}}>
                            <ExpansionPanel elevation={5} classes={{root:classes.expansionPanel, expanded:classes.temp2}}>
                                <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />} styles={{marginRight: '2vw', marginLeft: '2vw'}}>
                                    Beginner
                                </ExpansionPanelSummary>
                                <ExpansionPanelDetails styles={{marginRight: '2vw', marginLeft: '2vw'}}>
                                    <FormControl component="fieldset" >
                                        <Grid container direction='row'>
                                            {this.beginner_topics.map((topic) => {
                                                return <FormControlLabel 
                                                    classes={{label: classes.temp2}}
                                                    value={topic}
                                                    control={<Checkbox color="primary" />}
                                                    label={topic}
                                                    labelPlacement="start"
                                                    onChange={this.onClick}
                                                />
                                            })}
                                        </Grid>
                                    </FormControl>    
                                </ExpansionPanelDetails>
                            </ExpansionPanel>
                        </Grid>
                        <Grid item>
                            <ExpansionPanel classes={{root:classes.expansionPanel, expanded:classes.temp2}} elevation={5}>
                                <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />} styles={{marginRight: '2vw', marginLeft: '2vw'}}>
                                    Intermediate
                                </ExpansionPanelSummary>
                                <ExpansionPanelDetails styles={{marginRight: '2vw', marginLeft: '2vw'}}>
                                    <FormControl component="fieldset" >
                                        <Grid container direction='row'>
                                            {this.intermediate_topics.map((topic) => {
                                                return <FormControlLabel 
                                                    classes={{label: classes.temp2}}
                                                    value={topic}
                                                    control={<Checkbox color="primary" />}
                                                    label={topic}
                                                    labelPlacement="start"
                                                    onChange={this.onClick}
                                                />
                                            })}
                                        </Grid>
                                    </FormControl>    
                                </ExpansionPanelDetails>
                            </ExpansionPanel>
                        </Grid>
                        <Grid item>
                            <ExpansionPanel classes={{root:classes.expansionPanel, expanded:classes.temp2}} elevation={5} >
                                <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />} styles={{marginRight: '2vw', marginLeft: '2vw'}}>
                                    Advanced
                                </ExpansionPanelSummary>
                                <ExpansionPanelDetails styles={{marginRight: '2vw', marginLeft: '2vw'}}>
                                    <FormControl component="fieldset" >
                                        <Grid container direction='row'>
                                            {this.advanced_topics.map((topic) => {
                                                return <FormControlLabel 
                                                    classes={{label: classes.temp2}}
                                                    value={topic}
                                                    control={<Checkbox color="primary" />}
                                                    label={topic}
                                                    labelPlacement="start"
                                                    onChange={this.onClick}
                                                />
                                            })}
                                        </Grid>
                                    </FormControl>    
                                </ExpansionPanelDetails>
                            </ExpansionPanel>
                        </Grid>

                    </Grid>

                    <Grid item>
                        <Grid container spacing={4}>
                            <Grid item><Button className={classes.loginButton} variant="contained"  onClick={this.getArticleId}>Generate article!</Button></Grid>
                            <Grid item><Button component={Link} to={{pathname: "/doc", state: {articleId: this.state.articleId}}} classes={{root: classes.loginButton, disabled: classes.loginButtonDisabled}} variant="contained" disabled={!this.state.articlePrepared}>Continue</Button></Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </div>
        )
    }
})