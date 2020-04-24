import React from 'react';
import Button from '@material-ui/core/Button';
import { Grid } from '@material-ui/core';
import Paper from '@material-ui/core/Paper';
import { withStyles } from '@material-ui/core/styles';
import {Link} from "react-router-dom";
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import FindInPageIcon from '@material-ui/icons/FindInPage';
import TextField from '@material-ui/core/TextField';
import TableHead from '@material-ui/core/TableHead';
import TableSortLabel from '@material-ui/core/TableSortLabel';
import Tooltip from '@material-ui/core/Tooltip';
import axios from 'axios';
import Typography from '@material-ui/core/Typography';

// component styles
const styles = theme => ({
    button: {
        color: '#2268B2',
        border: 'solid',
        borderColor: '#9CBDD2',
        backgroundColor: "#f5f5f5",
        fontSize: '1em',
        marginBottom: '3vh',
        marginTop: '10vh',
        textAlign: 'center'
    },
    buttonDisabled: {
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
        marginBottom: '10vh',        
    },
    table: {
        width: '70vw',
        alignItems: 'center'
    },
    documentIcon: {
        color: '#2268B2'
    },
    searchUnderline: {
        color: '#2268B2',
    },
    searchFieldLabel: {
        color: '#4c5152'
    },
    searchField: {
        color: '#2268B2'
    },
    searchGrid: {
        marginTop: '1vh',
        marginRight: '1vw'
    },
    searchAndIconGrid: {
        marginBottom: '2vh'
    },
    labelCell: {
        textAlign: 'center'
    },
    sortTooltip: {
        color: '#2268B2 !important' 
    },
    titleCell: {
        width: '20vw',
        textDecoration: 'none',
        marginBottom: '1vh'
    },
    subtitleCell: {
        width: '15vw',
        textDecoration: 'none'
    },
    authorCell: {
        width: '10vw',
        textDecoration: 'none'
    },
    urlCell: {
        width: '15vw'
    },
    tableRow: {
        textDecoration: 'none'
    },
    loadingText: {
        color: '#2268B2',
        marginTop: '4vh',
        marginBottom: '4vh'
    }
})

// labels for use in the creation of the documents table
const labels = [
    {id: 'title', numeric: false, disablePadding: false, label: 'Title'},
    {id: 'subtitle', numeric: false, disablePadding: true, label: 'Subtitle'},
    {id: 'author', numeric: false, disablePadding: false, label: 'Author'},
    {id: 'link', numeric: false, disablePadding: false, label: 'Link'}
];

// a sorter helper function for stably sorting a list of objects
function stableSort(array, cmp) {
    const stabilizedThis = array.map((el, index) => [el, index]);
    stabilizedThis.sort((a,b) => {
        const order = cmp(a[0], b[0]);
        if (order != 0) return order;
        return a[1] - b[1];
    });
    return stabilizedThis.map(el => el[0]);
}

// a comparator helper function to determine the order of two objects
function desc(a, b, orderBy) {
    if (b[orderBy] < a[orderBy]) return -1;
    if (b[orderBy] > a[orderBy]) return 1;
    return 0;
}

// a helper function to facilitate the document sorting using the desc() function above
function getSorting(order, orderBy) {
    return order === 'desc' ? (a,b) => desc(a,b,orderBy) : (a,b) => -desc(a,b,orderBy);
}

// a helper function to truncate a string. Adapted from: https://medium.com/@DylanAttal/truncate-a-string-in-javascript-41f33171d5a8
function truncateString(str) {
    // if length is less than some threshold, returns full string
    if (str.length <= 50) {
      return str
    }

    // else, returns truncated string with '...' appended
    var temp = str.slice(0, 100);
    var ind = temp.lastIndexOf(' ');
    return temp.substring(0, ind) + '...';
  }

  // component that holds and enables engagement with a sortable table of documents seen by the user
export default withStyles(styles)(class MyDocumentsPage extends React.Component {

    state = {
        orderBy: 'title', // feature by which to order
        order: 'asc', // sorting order
        search: "", // search term
        docs: [] // documents to display
    }

    // retreieves documents by the user email and search field from DB
    getDocuments = async(display) => {
        // only shows display if first time reaching page
        if (display)
            this.setState({...this.state, isFetching: true});

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

            // converts each document to JS dictionary
            var conv_docs = {}
            for (var key in documents) {
                conv_docs[key] = JSON.parse(documents[key]);
            }

            // converts dictionary into a list
            var doc_list = []
            for (var key in conv_docs) {
                doc_list.push(conv_docs[key]);
            }

            this.setState({docs: doc_list, isFetching: false});
        })
    } 

    // on mount, attempts to retrieve documents from the DB
    componentDidMount() {
        this.getDocuments(true);
    }

    // alters the state to take into account updated search term
    handleSearchChange = (e) => {
        this.setState({search: e.target.value}, () => this.getDocuments(false));
    }

    // initiates a sort using current state
    handleRequestSort = property => event => {
        const orderBy = property;
        let order = 'desc';

        if (this.state.orderBy === property && this.state.order === 'desc') order = 'asc';
        this.setState({order, orderBy});
    };

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
                        <Paper rounded elevation={10} className={classes.titlePaper}>
                            <Typography style={{paddingTop: '4.5vh'}} variant="h3">My Documents</Typography>
                        </Paper>
                    </Grid>
                    <Paper className={classes.table}>
                        <Grid container direction="row" spacing="1" item justify="flex-end" alignItems="flex-end" className={classes.searchAndIconGrid}>
                            <Grid item><FindInPageIcon className={classes.documentIcon}/></Grid>
                            <Grid item className={classes.searchGrid}><TextField InputLabelProps={{classes: {root: classes.searchFieldLabel}}} InputProps={{classes: {input: classes.searchField, underline: classes.searchUnderline}}} className={classes.searchField} label="Search for documents..." onKeyUp={this.handleSearchChange} /></Grid>
                        </Grid>
                        <Table>
                            <TableHead>
                                <TableRow>
                                    {labels.map((label) => {
                                        return (
                                            <TableCell
                                                key={label.id}
                                                className={classes.labelCell}
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
                                                        onClick={this.handleRequestSort(label.id)}
                                                        classes={{icon: classes.sortTooltip}}
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
                                                tabIndex={-1}
                                                key={n._id}
                                                className={classes.tableRow}
                                            >
                                                <TableCell align="center" className={classes.titleCell} component={Link} to={{pathname: "/doc", state: {articleId: n._id}}} >{"\"" + n.title + "\""}</TableCell>
                                                <TableCell align="center" className={classes.subtitleCell} component={Link} to={{pathname: "/doc", state: {articleId: n._id}}} >{"\"" + truncateString(n.subtitle) + "\""}</TableCell>
                                                <TableCell align="center" className={classes.authorCell} component={Link} to={{pathname: "/doc", state: {articleId: n._id}}}>{n.author ? n.author : "Not available."}</TableCell>
                                                <TableCell align="center" className={classes.urlCell}><a href={n.link} target="_blank">Visit on the original site!</a></TableCell>
                                            </TableRow>
                                        )
                                    })
                                } 
                            </TableBody>
                        </Table>
                        <Grid container direction="row" spacing="1" item justify="center" alignItems="center">
                            <Grid item><Typography className={classes.loadingText} variant="h4">{this.state.isFetching ? 'Fetching documents...' : ''}</Typography></Grid>
                        </Grid>
                        
                    </Paper>

                    <Grid item>
                        <Grid container spacing={4}>
                        <Grid item><Button component={Link} to="/dash" classes={{root: classes.button, disabled: classes.buttonDisabled}} variant="contained">
                            <Typography variant="button">Back to Learning Center</Typography></Button></Grid>
                        </Grid>
                        
                    </Grid>
                    </Grid>
                </div>
            )
        }
    })