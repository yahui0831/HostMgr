import React from "react";
import {
    BrowserRouter as Router,
    Route
}from 'react-router-dom';
import {observer} from 'mobx-react-lite'
import {LoginForm, RegisterForm, Head} from './User'
import HostList from "./HostMgr"
import { user } from "./store";
import './App.css'

const App = observer(function App() {
  const mainPage = user.raw === null ? LoginForm : HostList;

  return (
    <div>
      <Head/>
      <Router>
        <Route exact path="/" component={mainPage}></Route>
        <Route path="/register" component={RegisterForm}></Route>
      </Router>
    </div>
  );
})

export default App;
