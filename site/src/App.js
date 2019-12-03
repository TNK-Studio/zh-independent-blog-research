import React from "react";
import Graph from "./components/Graph";
import Search from './components/Search';
import SiteCard from './components/SiteCard'


import { AppContextProvider } from './Context'


export default function App() {
  return (<>
    <AppContextProvider>
      <Search />
      <div style={{ display: 'flex', height: '95%' }}>
        <div style={{ position: 'absolute', zIndex: 10 }}>
          <SiteCard />
        </div>
        <Graph />
      </div>
    </AppContextProvider>
  </>);
}