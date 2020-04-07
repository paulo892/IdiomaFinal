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
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import FolderIcon from '@material-ui/icons/Folder';
import TableRow from '@material-ui/core/TableRow';
import Avatar from '@material-ui/core/Avatar';
import FindInPageIcon from '@material-ui/icons/FindInPage';
import TextField from '@material-ui/core/TextField';
import TableHead from '@material-ui/core/TableHead';
import Toolbar from '@material-ui/core/Toolbar';
import TableSortLabel from '@material-ui/core/TableSortLabel';
import Tooltip from '@material-ui/core/Tooltip';





import Checkbox from '@material-ui/core/Checkbox';
import axios from 'axios';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';
import Typography from '@material-ui/core/Typography';

import logo from "../images/logo.png";
import number_1 from "../images/number_1.png";
import number_2 from "../images/number_2.png";
import beginner from "../images/beginner.png";

const achievement_to_art = {
    "5dd603c61c9d4400004cadd8": number_1,
    "5dd604231c9d4400004cadda": number_2,
    "5e655fb81c9d440000df11a1": beginner
}


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
        backgroundColor: '#7AB4D8',
        height: 'auto'
    },
    questionPaper: {
        marginTop: '25vh',
        color: '#2268B2',
        fontFamily: 'Karla, sans-serif',
        //paddingTop: '0.5vh',
        paddingRight: '5vw',
        borderColor: '#2268B2',
        paddingLeft: '5vw',
        height: '15vh',
        backgroundColor: '#f5f5f5',
        //paddingBottom: '2vh',
        marginBottom: '10vh',
        //width: '50vw'.
        
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
        /*border: 'solid',
        borderStyle: 'solid',
        borderColor: '#2268B2',*/
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
    achievementIcon: {
        height: '10vh',
        width: '10vh'
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
    table: {
        width: '60vw'
    },
    documentIcon: {
        color: '#2268B2'
    },
    searchUnderline: {
        color: '#2268B2'
    },
    searchFieldLabel: {
        color: '#4c5152'
    },
    searchField: {
        color: '#2268B2'
    },
})


// TODO - Look into way to make this dynamic
const labels = [
    {id: 'title', numeric: false, disablePadding: false, label: 'Title'},
    {id: 'subtitle', numeric: false, disablePadding: true, label: 'Subtitle'},
    {id: 'author', numeric: false, disablePadding: false, label: 'Author'},
    {id: 'link', numeric: false, disablePadding: false, label: 'Link'}
];

function stableSort(array, cmp) {
    const stabilizedThis = array.map((el, index) => [el, index]);
    stabilizedThis.sort((a,b) => {
        const order = cmp(a[0], b[0]);
        if (order != 0) return order;
        return a[1] - b[1];
    });
    return stabilizedThis.map(el => el[0]);
}

function desc(a, b, orderBy) {
    if (b[orderBy] < a[orderBy]) return -1;
    if (b[orderBy] > a[orderBy]) return 1;
    return 0;
}

function getSorting(order, orderBy) {
    return order === 'desc' ? (a,b) => desc(a,b,orderBy) : (a,b) => -desc(a,b,orderBy);
}

export default withStyles(styles)(class AchievementsPage extends React.Component {

    state = {
        orderBy: 'title',
        order: 'asc',
        search: "",
        docs: []
    }

    getDocuments = async() => {
        // TODO - implement back-end
        await axios.get(
            '/api/getUserDocuments',
            {
                params: {
                    search: this.state.search,
                    email: this.props.email
                }
            },
            {
                headers: {'Content-type': 'application/json'}
            }
        ).then((data) => {
            // saves the documents
            let documents = data['data'];
            console.log(documents);

            // converts each document to JS dictionary
            var conv_docs = {}
            for (var key in documents) {
                console.log(key);
                conv_docs[key] = JSON.parse(documents[key]);
            }

            // converts dictionary into a list
            var doc_list = []
            for (var key in conv_docs) {
                doc_list.push(conv_docs[key]);
            }
            console.log(doc_list)

            this.setState({docs: doc_list});
        })
    } 

    componentDidMount() {
        this.getDocuments();
    }

    handleSearchChange = (e) => {
        //this.setState({search: e.target.value});

        //this.getDocuments();
    }

    handleRequestSort = (event, property) => {
        const orderBy = property;
        let order = 'desc';

        if (this.state.orderBy === property && this.state.order === 'desc') order = 'asc';
        this.setState({order, orderBy});
    };

    // TODO - potentially remove this function to consolidate
    createSortHandler = property => event => {
        // TODO
        console.log('SORT');

        this.handleRequestSort(event, property);
    }

    isSelected = property => {
        console.log('success');
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
                            <Typography style={{paddingTop: '4.5vh'}} variant="h3">My Documents</Typography>
                        </Paper>
                    </Grid>
                    <Paper className={classes.table}>
                        <Grid container direction="row" spacing="1" item justify="flex-end" alignItems="flex-end">
                            <Grid item><FindInPageIcon className={classes.documentIcon}/></Grid>
                            <Grid item><TextField InputLabelProps={{classes: {root: classes.searchFieldLabel}}} InputProps={{classes: {input: classes.searchField, underline: classes.searchUnderline}}} className={classes.searchField} label="Search for documents..." onKeyUp={this.handleSearchChange} /></Grid>
                        </Grid>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    {labels.map((label) => {
                                        return (
                                            <TableCell
                                                key={label.id}
                                                numeric={label.numeric}
                                                padding={'none'}
                                                sortDirection={this.state.orderBy === label.id ? this.state.order : false}
                                            >
                                                <Tooltip
                                                    title="Sort"
                                                    placement={label.numeric ? 'bottom-end' : 'bottom-start'}
                                                >
                                                    <TableSortLabel
                                                        active={this.state.orderBy === label.id && !(label.id === 'link')}
                                                        direction={this.state.order}
                                                        onClick={this.createSortHandler(label.id)}
                                                    >
                                                        <Typography style={{color: '#3D8AC8'}} variant="h6">{label.label}</Typography>
                                                    </TableSortLabel>
                                                </Tooltip>
                                            </TableCell>
                                        );
                                    })}
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {
                                    stableSort(this.state.docs, getSorting(this.state.order, this.state.orderBy)).map(n => {
                                        return (
                                            <TableRow
                                                hover
                                                onClick={event => this.isSelected(n._id)}
                                                tabIndex={-1}
                                                key={n._id}
                                                /*component={Link} to={ TODO}*/

                                            >
                                                <TableCell align="center">{n.title}</TableCell>
                                                <TableCell align="center">{n.subtitle}</TableCell>
                                                <TableCell align="center">{n.author}</TableCell>
                                                <TableCell align="center">{n.link}</TableCell>
                                            </TableRow>
                                        )
                                    })
                                }
                            </TableBody>
                        </Table>
                    </Paper>

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

    //<Grid item><Button component={Link} to={{pathname: "/doc", state: {articleId: this.state.articleId}}} classes={{root: classes.loginButton, disabled: classes.loginButtonDisabled}} variant="contained" disabled={!this.state.articlePrepared}>Continue</Button></Grid>
