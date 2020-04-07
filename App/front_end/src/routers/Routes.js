import React, { Component }  from 'react';
import {BrowserRouter, Router, Route, Switch, Redirect, withRouter} from 'react-router-dom';
import Home from '../components/Home';
import Callback from '../auth/CallBack';
import Auth from '../auth/auth';
import history from '../auth/history';
import LoginPage from '../components/LoginPage'
import NavBar from '../components/NavBar'
import { createMuiTheme } from '@material-ui/core/styles';
import {Link} from "react-router-dom";
import { ThemeProvider } from '@material-ui/styles';
import Dashboard from '../components/Dashboard';
import DocumentPageFT from '../components/DocumentPageFT'
import DocumentPage from '../components/DocumentPage'
import { useAuth0 } from "../react-auth0-spa";
import Temp from '../components/Temp';
import AchievementsPage from '../components/AchievementsPage';
import MyDocumentsPage from '../components/MyDocumentsPage';

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

const auth = new Auth();

const handleAuthentication = (nextState, replace) => {
  if (/access_token|id_token|error/.test(nextState.location.hash)) {
    auth.handleAuthentication();
  }
}

function Routes() {
  const { loading , user} = useAuth0();

  if (loading) {
    return <div>Loading...</div>;
  }

  return (<div>
    <ThemeProvider theme={theme}>
      <Router history={history} component={Home}>
        <div>
          <NavBar auth={auth} />
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
