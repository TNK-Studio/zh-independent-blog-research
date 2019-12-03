import React, { Suspense, lazy } from "react";
import Graph from "./components/Graph";
import AppBar from './components/AppBar';
import SiteCard from './components/SiteCard'
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";


import { AppContextProvider } from './Context'

const Report = lazy(() => import('./pages/report'))

export default function App() {
  return (<Router>
    <AppContextProvider>
      <AppBar />
      <Suspense fallback={<div>Loading...</div>}>
        <Switch>
          <Route path="/report">
            <Report />
          </Route>
          <Route path="/">
            <div style={{ height: '100%' }}>
              <div style={{ display: 'flex', height: '95%' }}>
                <div style={{ position: 'absolute', zIndex: 10 }}>
                  <SiteCard />
                </div>
                <Graph />
              </div>
            </div>
          </Route>
        </Switch>
      </Suspense>
    </AppContextProvider>
  </Router>);
}