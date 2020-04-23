import createHistory from 'history/createBrowserHistory';

// a helper function for Auth0 authentication
export default createHistory({
  basename: '/'
});