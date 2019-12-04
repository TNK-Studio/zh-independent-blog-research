import React, { Suspense, lazy } from "react";
import Graph from "./components/Graph";
import AppBar from './components/AppBar';
import SiteCard from './components/SiteCard'
import SearchList from './components/SearchList'

import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";


import { AppContextProvider } from './Context'

const Report = lazy(() => import('./pages/report'))
const About = lazy(() => import('./pages/about'))

export default function App() {
  return (<Router>
    <AppContextProvider>
      <AppBar />
      <div style={{ paddingTop: 64, height: 'calc(100% - 64px)' }}>
        <Suspense fallback={<div style={{ margin: '0 auto', textAlign: 'center' }}>Loading...</div>}>
          <Switch>
            <Route path="/report">
              <Report />
            </Route>
            <Route path="/about">
              <About />
            </Route>
            <Route path="/">
              <div style={{ height: '100%' }}>
                <div style={{ display: 'flex', height: '100%' }}>
                  <div style={{ position: 'absolute', zIndex: 10 }}>
                    <SiteCard />
                    <SearchList />
                  </div>
                  <Graph />
                </div>
              </div>
            </Route>
          </Switch>
        </Suspense>
      </div>
    </AppContextProvider>
  </Router>);
}