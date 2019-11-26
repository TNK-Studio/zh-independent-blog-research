import React, { useState } from "react";
import Graph from "react-graph-vis";
import graph from "./graph.json"
import data from "./data.json"

export default function App() {
  // const graph = data
  const [network, setNetwork] = useState({})
  const options = {
    nodes: {
      shape: "dot",
      size: 16
    },
    edges: {
      width: 0.15,
      color: { inherit: "from" },
      smooth: {
        type: "continuous"
      }
    },
    physics: {
      forceAtlas2Based: {
        gravitationalConstant: -26,
        centralGravity: 0.005,
        springLength: 230,
        springConstant: 0.18
      },
      maxVelocity: 50,
      minVelocity: 0.1,
      solver: "forceAtlas2Based",
      timestep: 0.35,
      stabilization: { iterations: 150 }
    },
    interaction: {
      // hideNodesOnDrag: true,
      hideEdgesOnDrag: true,
      tooltipDelay: 200,
      hover: true
    },
    // physics: false
  };

  const events = {
    select: function (event) {
      var { nodes, edges } = event;
      console.log(nodes, edges)
    }
  };
  return (<>
    <div>
      search
    </div>
    <Graph
      graph={graph}
      options={options}
      events={events}
      getNetwork={network => {
        setNetwork(network)
        //  if you want access to vis.js network api you can set the state in a parent component using this property
      }}
    />
  </>);
}