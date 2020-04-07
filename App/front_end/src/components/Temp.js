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
import {Link} from "react-router-dom";

import Checkbox from '@material-ui/core/Checkbox';
import axios from 'axios';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';
import Typography from '@material-ui/core/Typography';

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
    headerPaper: {
        marginTop: '25vh',
        color: '#2268B2',
        paddingTop: '6vh',
        paddingRight: '3vw',
        paddingLeft: '3vw',
        backgroundColor: '#f5f5f5',
        paddingBottom: '3vh',
        width: '50vw'
    },
    textPaper: {
        marginTop: '5vh',
        color: '#2268B2',
        paddingTop: '1vw',
        paddingRight: '3vw',
        borderColor: '#2268B2',
        paddingLeft: '3vw',
        backgroundColor: '#f5f5f5',
        paddingBottom: '3vh',
        width: '50vw'
    },
    backgroundDiv: {
        backgroundColor: '#58ABDE',
        height: 'auto'
    }
})





export default withStyles(styles)(class Temp extends React.Component {

    state = {
        attributes: [],
        article: null
    }

    componentDidMount() {
        axios.get(
            '/api/getArticleData',
            {
                params: {
                    articleId: this.props.articleId
                }
                
            },
            {
                headers: {'Content-type': 'application/json'}
            }
        ).then((data) => {
            const result = data['data'];
            console.log(result);
            this.setState({article: result});
            
        })
    }

    updateUser = async() => {
        console.log('sifsjf');
        console.log(this.state.article['_id']);
        await axios.post(
            '/api/updateUser',
            {
                articleViewed: this.state.article['_id'],
                articleFeatures: this.state.article['features'],
                email: this.props.email
                
            },
            {
                headers: {'Content-type': 'application/json'}
            }
        ).then((data) => {
            console.log('Done');
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
                
                    <Paper rounded elevation={10} className={classes.headerPaper}>
                        <div>Hello</div>
                    </Paper>

                    <Grid item>
                        <Grid container spacing={4}>
                        <Grid item><Button component={Link} to="/dash" classes={{root: classes.loginButton, disabled: classes.loginButtonDisabled}} variant="contained">
                            <Typography variant="button">Continue</Typography></Button></Grid>
                        </Grid>
                        
                    </Grid>
                </Grid>
            </div>
        )
    }
})

//<Grid item><Button component={Link} to={{pathname: "/doc", state: {articleId: this.state.articleId}}} classes={{root: classes.loginButton, disabled: classes.loginButtonDisabled}} variant="contained" disabled={!this.state.articlePrepared}>Continue</Button></Grid>
