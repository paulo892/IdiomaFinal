import React from 'react';
import Button from '@material-ui/core/Button';
import { Grid } from '@material-ui/core';
import Paper from '@material-ui/core/Paper';
import { withStyles } from '@material-ui/core/styles';
import {Link} from "react-router-dom";
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableRow from '@material-ui/core/TableRow';
import Avatar from '@material-ui/core/Avatar';
import axios from 'axios';
import Typography from '@material-ui/core/Typography';
import logo from "../images/logo.png";
import number_1 from "../images/number_1.png";
import number_2 from "../images/number_2.png";
import beginner from "../images/beginner.png";

// mapping for each achievement to an icon image
const achievement_to_art = {
    "5dd603c61c9d4400004cadd8": number_1,
    "5dd604231c9d4400004cadda": number_2,
    "5e655fb81c9d440000df11a1": beginner
}

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
        marginBottom: '15vh',
        marginTop: '5vh',
        textAlign: 'center'
    },
    backgroundDiv: {
        backgroundColor: '#7AB4D8',
        height: 'auto'
    },
    questionPaper: {
        marginTop: '22vh',
        color: '#2268B2',
        fontFamily: 'Karla, sans-serif',
        paddingRight: '5vw',
        borderColor: '#2268B2',
        paddingLeft: '5vw',
        height: '15vh',
        backgroundColor: '#f5f5f5',
        marginBottom: '10vh'     
    },
    achievementsPaper: {
        color: '#2268B2',
        fontFamily: 'Karla, sans-serif',
        width: '50vw',
        paddingLeft: '2vw',
        paddingRight: '2vw',
        paddingTop: '4vh',
        paddingBottom: '4vh',
        marginBottom: '4vh'
    },
    achievementRow: {
        height: '15vh',
    },
    achievementBadge: {
        height: '15vh',
        width: '15vh',
        border: 'solid',
        borderStyle: 'solid',
        borderColor: '#2268B2',
        backgroundColor: 'white'
    },
    pointsBadge: {
        height: '12vh',
        width: '12vh',
        backgroundColor: '#2268B2',
        color: 'white',
    },
    badgeImage: {
        height: '13vh'
    },
    loadingPaper: {
        height: '10vh',
        width: '25vw',
        textAlign: 'center'
    },
    loadingText: {
        color: '#2268B2',
        marginTop: '4vh',
        marginBottom: '4vh',
        paddingTop: '3vh'
    }
})

// component to display system achievements, both those unlocked and still in progress for the user
export default withStyles(styles)(class AchievementsPage extends React.Component {

    state = {
        user_achievements: null, // user-achieved achievements
        rem_achievements: null // remaining achievements
    }

    // after mount, gets the user's achievements, all achievements, and portions them into lists
    componentDidMount() {
        this.setState({...this.state, isFetching: true});

        // retrieves the user achievements
        axios.get(
            '/api/getUserAchievements',
            {
                params: {email: this.props.email}
                
            },
            {
                headers: {'Content-type': 'application/json'}
            }
        ).then((data) => {
            // saves the user's achievements
            const user_ach = data['data'];

            // gets all possible achievements
            axios.get(
                '/api/getAllAchievements',
                {
                    headers: {'Content-type': 'application/json'}
                }
            ).then((data) => {
                // saves all possible achievements
                const all_ach = data['data'];
                var rem_ach = {};

                // for each possible achievement...
                for (var key in all_ach) {
                    // skips if user has achieved it
                    if (key in user_ach) {
                        continue;
                    }
                    // else, adds it to list of remaining achievements
                    else {
                        rem_ach[key] = all_ach[key];
                    }
                }

                // converts strings to JS dictionaries
                var conv_user_ach = {}
                for (var ach in user_ach) {
                    conv_user_ach[ach] = JSON.parse(user_ach[ach]);
                }

                var conv_rem_ach = {}
                for (var ach in rem_ach) {
                    conv_rem_ach[ach] = JSON.parse(rem_ach[ach]);
                }

                // updates the two lists in state
                this.setState({user_achievements: conv_user_ach, rem_achievements: conv_rem_ach, isFetching: false});
            })
        })
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
                    direction="column"
                    alignItems="center"
                    justify="center"
                >
                    <Paper rounded elevation={10} className={classes.questionPaper}>
                        <Typography style={{paddingTop: '4.5vh'}} variant="h3">Achievements</Typography>
                    </Paper>
                </Grid>
                {this.state.isFetching ? <Grid container direction="row" spacing="1" item justify="center" alignItems="center">
                    <Grid item><Paper className={classes.loadingPaper}><Typography className={classes.loadingText} variant="h4">{'Fetching achievements...'}</Typography></Paper></Grid>
                </Grid> : <div></div>}
                <Grid item>
                    <Table>
                        <TableBody>
                            {(this.state.user_achievements) ? Object.values(this.state.user_achievements).map(n => {
                                return (
                                    <TableRow  className={classes.achievementRow}>
                                        <Paper style={{backgroundColor: '#f5f5f5'}} rounded elevation={10} className={classes.achievementsPaper}>
                                            <Grid container spacing={4}>
                                                <Grid item >
                                                    <Avatar className={classes.achievementBadge} ><img src={achievement_to_art[n['_id']]} className={classes.badgeImage}></img></Avatar>
                                                </Grid>
                                                <Grid item xs ={12} sm container>
                                                    <Grid item xs container direction="column" spacing={1}>
                                                        <Grid item xs>
                                                            <Typography style={{fontStyle: 'italic', fontWeight: 'bold'}} variant="h4">"{n['name']}"</Typography>
                                                        </Grid>
                                                        <Grid item xs>
                                                            <Typography style={{color: '#3D8AC8'}} variant="h6">{n['desc']}</Typography>
                                                        </Grid>
                                                        <Grid item xs>
                                                            <Typography style={{color: '#3D8AC8'}} variant="subtitle1">Acquired: {n['date_achieved']}</Typography>
                                                        </Grid>
                                                    </Grid>   
                                                </Grid>
                                                <Grid item  direction="column" alignItems="center" alignContent="center" justify="center">
                                                    <Avatar border={1} className={classes.pointsBadge} style={{marginTop: '2vh'}} variant="rounded">
                                                        <Typography style={{fontWeight: 'bold'}} variant="h4">+{n['pts']}</Typography>
                                                    </Avatar>
                                                </Grid>
                                            </Grid>
                                        </Paper>
                                    </TableRow>
                                    
                                )
                            }) : <div></div>}
                            {(this.state.rem_achievements) ? Object.values(this.state.rem_achievements).map(n => {
                                return (
                                    <TableRow  className={classes.achievementRow}>
                                        <Paper style={{backgroundColor: '#f5f5f5', filter: 'grayscale(100%)'}} rounded elevation={10} className={classes.achievementsPaper}>
                                            <Grid container spacing={4}>
                                                <Grid item >
                                                <Avatar className={classes.achievementBadge} ><img src={achievement_to_art[n['_id']]} className={classes.badgeImage}></img></Avatar>
                                                </Grid>
                                                <Grid item xs ={12} sm container>
                                                    <Grid item xs container direction="column" spacing={1}>
                                                        <Grid item xs>
                                                            <Typography style={{fontStyle: 'italic', fontWeight: 'bold'}} variant="h4">"{n['name']}"</Typography>
                                                        </Grid>
                                                        <Grid item xs>
                                                            <Typography style={{color: '#3D8AC8'}} variant="h6">{n['desc']}</Typography>
                                                        </Grid>
                                                        <Grid item xs>
                                                            <Typography style={{color: '#3D8AC8'}} variant="subtitle1">Acquired: {n['date_achieved']}</Typography>
                                                        </Grid>
                                                    </Grid>   
                                                </Grid>
                                                <Grid item  direction="column" alignItems="center" alignContent="center" justify="center">
                                                    <Avatar border={1} className={classes.pointsBadge} style={{marginTop: '2vh'}} variant="rounded">
                                                        <Typography style={{fontWeight: 'bold'}} variant="h4">+{n['pts']}</Typography>
                                                    </Avatar>
                                                </Grid>
                                            </Grid>
                                        </Paper>
                                    </TableRow>
                                    
                                )
                            }) : <div></div>}
                        </TableBody>
                    </Table>
                </Grid>

                <Grid item>
                    <Grid container spacing={4}>
                    <Grid item><Button component={Link} to="/dash" classes={{root: classes.loginButton, disabled: classes.loginButtonDisabled}} variant="contained">
                        <Typography variant="button">Back to Learning Center</Typography></Button></Grid>
                    </Grid>
                    
                </Grid>
                </Grid>
            </div>
        )
    }
})