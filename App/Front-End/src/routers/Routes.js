import React from 'react';
import {Router, Route, Switch} from 'react-router-dom';
import { createMuiTheme } from '@material-ui/core/styles';
import { ThemeProvider } from '@material-ui/styles';
import Dashboard from '../components/Dashboard';
import DocumentPageFT from '../components/DocumentPageFT'
import DocumentPage from '../components/DocumentPage'
import { useAuth0 } from "../react-auth0-spa";
import AchievementsPage from '../components/AchievementsPage';
import MyDocumentsPage from '../components/MyDocumentsPage';
import Home from '../components/Home';
import Auth from '../auth/auth';
import history from '../auth/history';
import NavBar from '../components/NavBar'

// application theme
const theme = createMuiTheme({
  typography: {
    fontFamily: [
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"',
    ].join(','),
  },
});

// creates Auth object for authentication
const auth = new Auth();

// component that uses React Router to route the user to diff. screens
function Routes() {
  const { loading , user} = useAuth0();

  // displays loading screen if authentication processing
  if (loading) {
    return <div>Loading...</div>;
  }

  return (<div>
    <ThemeProvider theme={theme}>
      <Router history={history} component={Home}>
        <div>
          <NavBar auth={auth} email={user != null ? user.email : 'none'}/>
          <Switch>
            <Route exact path="/" render={(props) => <Home auth={auth}  {...props} />} />
            <Route path="/dash" render={(props) => <Dashboard auth={auth} email={user.email} {...props} />} />
            <Route path="/doc" render={(props) => <DocumentPage auth={auth} email={user.email} articleId={props.location.state.articleId} />} />
            <Route path="/docft" render={(props) => <DocumentPageFT auth={auth} email={user.email} articleId={props.location.state.articleId} />} />
            <Route path="/mydocs" render={(props) => <MyDocumentsPage auth={auth} email={user.email}/>} />
            <Route path="/achievements" render={(props) => <AchievementsPage auth={auth} email={user.email}/>} />
          </Switch>
        </div>
      </Router>
    </ThemeProvider></div>)

}

export default Routes;
