import React, { Component }  from 'react';
import {BrowserRouter, Router, Route, Switch, Redirect, withRouter} from 'react-router-dom';
import Home from '../components/Home';
import Callback from '../auth/CallBack';
import Auth from '../auth/auth';
import history from '../auth/history';
import LoginPage from '../components/LoginPage'
import NavBar from '../components/NavBar'

const auth = new Auth();

const handleAuthentication = (nextState, replace) => {
  if (/access_token|id_token|error/.test(nextState.location.hash)) {
    auth.handleAuthentication();
  }
}

class Routes extends Component {
  state = {
      auth: false
  };

  login = () => {
    auth.login();
    console.log('wfosjefo' + auth.isAuthenticated()); 
    this.setState({auth: auth.isAuthenticated()});
  }
  // calls the logout method in authentication service
  logout = () => {
    auth.logout();
    console.log('wfosjefo' + auth.isAuthenticated()); 
    this.setState({auth: auth.isAuthenticated()});
  }
  render() {
    return(
    <Router history={history} component={Home}>
    <div>
      <NavBar auth={auth} handleSubmit={this.logout}/>
      <Switch>
        <Route exact path="/" render={(props) => <Home auth={auth} handleSubmit={this.login} {...props} />} />
        <Route path="/home" render={(props) => <Home auth={auth} handleSubmit={this.logout} {...props} />} />
        <Route path="/callback" render={(props) => {
          console.log('there');
          handleAuthentication(props);
          return <Callback {...props} />
        }}/>
      </Switch>
    </div>
  </Router>);
  } 
}

export default Routes;