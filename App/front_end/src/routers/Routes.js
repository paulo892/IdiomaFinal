import React, { Component }  from 'react';
import {BrowserRouter, Router, Route, Switch, Redirect, withRouter} from 'react-router-dom';
import Home from '../components/Home';
import Callback from '../auth/CallBack';
import Auth from '../auth/auth';
import history from '../auth/history';
import LoginPage from '../components/LoginPage'
import NavBar2 from '../components/NavBar2';
import NavBar3 from '../components/NavBar3'
import { createMuiTheme } from '@material-ui/core/styles';
import { ThemeProvider } from '@material-ui/styles';
import Dashboard from '../components/Dashboard';
import { useAuth0 } from "../react-auth0-spa";

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
  const { loading } = useAuth0();

  if (loading) {
    return <div>Loading...</div>;
  }

  return (<div>
    <ThemeProvider theme={theme}>
      <Router history={history} component={Home}>
        <div>
          <NavBar3 auth={auth} />
          <Switch>
            <Route exact path="/" render={(props) => <Home auth={auth}  {...props} />} />
            <Route path="/home" render={(props) => <Home auth={auth}  {...props} />} />
            <Route path="/dash" render={(props) => <Dashboard auth={auth} {...props} />} />
            <Route path="/callback" render={(props) => {
              console.log('there');
              handleAuthentication(props);
              return <Callback {...props} />
            }}/>
          </Switch>
        </div>
      </Router>
    </ThemeProvider></div>)

}

export default Routes;
