import React, { Component } from 'react';
import LoginPage from './LoginPage';
import Dashboard from './Dashboard';

// component to encapsulate Auth0 logic and determine what page to show the user
class Home extends Component {

  // selects the displayed page based on user authentication
  render() {
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