import React from 'react';
import Button from '@material-ui/core/Button';
import { Grid } from '@material-ui/core';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Paper from '@material-ui/core/Paper';
import { withStyles } from '@material-ui/core/styles';
import Checkbox from '@material-ui/core/Checkbox';
import axios from 'axios';
import {Link} from "react-router-dom";
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import Typography from '@material-ui/core/Typography';
import logo from "../images/logo.png";

// component styles
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
        marginBottom: '3vh',
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
        marginBottom: '3vh',
        marginTop: '5vh',
        textAlign: 'center'
    },
    questionPaper: {
        marginTop: '5vh',
        color: '#2268B2',
        fontFamily: 'Karla, sans-serif',
        paddingTop: '1vw',
        paddingRight: '3vw',
        borderColor: '#2268B2',
        paddingLeft: '3vw',
        backgroundColor: '#f5f5f5',
        paddingBottom: '3vh',
        marginBottom: '5vh',
        width: '30vw',
        textAlign: 'center'
    },
    expansionPanel: {
        backgroundColor: '#f5f5f5',
        marginBottom: '3vh',
        color: '#2268B2',
        width: '15vw'
    },
    backgroundDiv: {
        backgroundColor: '#7AB4D8',
        height: 'auto',
        width: '100vw'
    },
    titlePaper: {
        marginTop: '22vh',
        color: '#2268B2',
        fontFamily: 'Karla, sans-serif',
        paddingRight: '5vw',
        borderColor: '#2268B2',
        paddingLeft: '5vw',
        height: '15vh',
        backgroundColor: '#f5f5f5',
        marginBottom: '5vh',        
    },
})

// component to allow a user to enter their desired learning criteria and generate such an article on the back-end
export default withStyles(styles)(class LoginPage extends React.Component {

    // article filter criteria
    beginner_topics = ['Números', 'Preposições', 'Superlativos', 'Interrogativos', "Presente Indicativo (Regular)", "Presente Indicativo (Irregular)", "Ser vs. Estar"];
    intermediate_topics = ["Pretérito Indicativo (Regular)", "Pretérito Indicativo (Irregular)", "Imperfeito (Regular)", "Imperfeito (Irregular)","Presente Gerúndio","Presente Subjuntivo (Regular)","Presente Indicativo (Irregular)"];
    advanced_topics = ["Passado Subjuntivo (Regular)","Passado Subjuntivo (Irregular)","Presente Perfeito","Pretérito Perfeito","Futúro Indicativo (Regular)","Futúro Indicativo (Irregular)","Futúro Perfeito","Condicional (Regular)","Condicional (Irregular)"];
    countries = ["Portugal", "Brazil", "Angola", "Mozambique"]
    subjects = ['Politics', 'Science', 'Technology', 'Economics', 'Culture']

    state = {
        attributes: [], // search filters
        experience: [], // user experience
        articleId: null, // generated article ID
        articlePrepared: false // boolean showing whether article has been prepared
    }

    // on mount, retrieves the user experience from the DB
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
            this.setState({experience: result});
        })
    }

    // retrieves a suitable article given the user criteria
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
            window.alert('Article ' + details + ' prepared! Ready to continue.' );

            if (details != 'a') {
                this.setState({articlePrepared: true, articleId: details})
            }
        })
    }

    // adds the attribute to the attribute list
    onClick = (e) => {
        let checked = e.target.checked;
        let val = e.target.value;
        let vals = this.state.attributes;

        if (checked) {
            vals.push(val);
            this.setState(() => ({
                attributes: vals
            }))
        }
        else {
            let i = this.state.attributes.indexOf(val);
            if (i > -1) {
                vals.splice(i, 1);
                this.setState(() => ({
                    attributes: vals
                }))
            }
        }
    }

    render() {

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
                    <Grid 
                        item
                        spacing={0}
                        alignItems="center"
                        justify="center"
                    >
                        <Paper rounded elevation={10} className={classes.titlePaper}>
                            <Typography style={{paddingTop: '4.5vh'}} variant="h3">Learning Center</Typography>
                        </Paper>
                    </Grid>

                    <Grid
                        container
                        direction="row"
                        alignItems="flex-start"
                        justify="center"
                    >
                        <Grid 
                            item container
                            spacing={0}
                            xs={6}
                            direction="column"
                            alignItems="center"
                            justify="center"
                        >
                            <Grid item justify="center">
                                <Paper rounded elevation={5} className={classes.questionPaper}>
                                    <Typography variant="h4">What would you like to learn about today?</Typography>
                                </Paper>
                            </Grid>
                            <Grid
                                container item
                                alignItems="center"
                                justify="center"
                            >
                                <Grid item xs={4} justify="center" styles={{marginRight: '2vw', marginLeft: '2vw'}}>
                                    <ExpansionPanel elevation={5} classes={{root:classes.expansionPanel, expanded:classes.temp2}}>
                                        <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />} styles={{marginRight: '2vw', marginLeft: '2vw'}}>
                                            <Typography variant="h5">Countries</Typography>
                                        </ExpansionPanelSummary>
                                        <ExpansionPanelDetails styles={{marginRight: '2vw', marginLeft: '2vw'}}>
                                            <FormControl component="fieldset" >
                                                <Grid container direction='row'>
                                                    {this.countries.map((topic) => {
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
                                <Grid item xs={4} justify="center">
                                    <ExpansionPanel classes={{root:classes.expansionPanel, expanded:classes.temp2}} elevation={5}>
                                        <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />} styles={{marginRight: '2vw', marginLeft: '2vw'}}>
                                        <Typography variant="h5">Topics</Typography>
                                        </ExpansionPanelSummary>
                                        <ExpansionPanelDetails styles={{marginRight: '2vw', marginLeft: '2vw'}}>
                                            <FormControl component="fieldset" >
                                                <Grid container direction='row'>
                                                    {this.subjects.map((topic) => {
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
                        </Grid>
                        <Grid 
                            item container
                            direction="column"
                            xs={6}
                            alignItems="center"
                            justify="center"
                        >
                            <Grid item>
                                <Paper rounded elevation={5} className={classes.questionPaper}>
                                    <Typography variant="h4">What subjects would you like to cover?</Typography>
                                </Paper>
                            </Grid>
                            <Grid
                                container item
                                alignItems="center"
                                justify="center"
                            >
                                <Grid item xs={4} styles={{marginRight: '2vw', marginLeft: '2vw'}}>
                                    <ExpansionPanel elevation={5} classes={{root:classes.expansionPanel, expanded:classes.temp2}}>
                                        <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />} styles={{marginRight: '2vw', marginLeft: '2vw'}}>
                                            <Typography variant="h5">Beginner</Typography>
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
                                <Grid item xs={4}>
                                    <ExpansionPanel classes={{root:classes.expansionPanel, expanded:classes.temp2}} elevation={5}>
                                        <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />} styles={{marginRight: '2vw', marginLeft: '2vw'}}>
                                        <Typography variant="h5">Intermediate</Typography>
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
                            </Grid>
                            <Grid
                                container item
                                alignItems="center"
                                justify="center"
                            >             
                                <Grid item xs={4}>
                                    <ExpansionPanel classes={{root:classes.expansionPanel, expanded:classes.temp2}} elevation={5} >
                                        <ExpansionPanelSummary expandIcon={<ExpandMoreIcon />} styles={{marginRight: '2vw', marginLeft: '2vw'}}>
                                            <Typography variant="h5">Advanced</Typography>
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
                        </Grid>

                    </Grid>
                    <Grid item>
                        <Grid container spacing={4}>
                            <Grid item><Button className={classes.loginButton} variant="contained"  onClick={this.getArticleId}>Generate article!</Button></Grid>
                            <Grid item><Button component={Link} to={{pathname: "/docft", state: {articleId: this.state.articleId}}} classes={{root: classes.loginButton, disabled: classes.loginButtonDisabled}} variant="contained" disabled={!this.state.articlePrepared}>Continue</Button></Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </div>
        )
    }
})