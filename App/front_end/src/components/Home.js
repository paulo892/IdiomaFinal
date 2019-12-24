import React, { Component } from 'react';
import App from '../App';
import LoginPage from './LoginPage';
import Dashboard from './Dashboard';

class Home extends Component {
  // calls the login method in authentication service
  render() {
    // calls the isAuthenticated method in authentication service
    const { isAuthenticated } = this.props.auth;
    return (
      <div>
        {
          !isAuthenticated() &&
          <LoginPage submitBehavior={this.props.handleSubmit}/>
        }
        {
          isAuthenticated() &&
          <Dashboard submitBehavior={this.props.handleSubmit}/>
        }
      </div>
      );
    }
  }

  export default Home;