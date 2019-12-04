import React, { useState, useContext } from "react";
import Graph from "react-graph-vis";
import graph from "../graph.json"
import { AppContext, domainDataMap } from '../Context'


export default function NetworkGraph() {
    const [network, setNetwork] = useState({})
    const [maxNodeNum] = useState(() => {
        return parseInt(localStorage.getItem("maxNodeNum"))
    })
    const { state, dispatch } = useContext(AppContext)
    const { graphData } = state

    let _graphData

    if (graphData) {
        _graphData = graphData
    } else {
        if (graph.nodes.length > maxNodeNum) {
            graph.nodes = graph.nodes.slice(0, maxNodeNum)
            // let allUrls = new Set(graph.nodes.map(node => node.id))
            // console.log(allUrls)
            // graph.edges = graph.edges.filter(edges => {
            //     const { from, to } = edges
            //     // console.log(from, to)
            //     return allUrls.has(from) && allUrls.has(to)
            // })
        }
        console.log(graph)
        _graphData = graph
    }
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
            // console.log(nodes, edges)
        },
        click: function (event) {
            var { nodes, edges } = event;
            // console.log(nodes, edges)
            if (nodes.length > 0) {
                // window.open(nodes[0]);
                let selectedURL = new URL(nodes[0])
                let selectedSite = domainDataMap[selectedURL.hostname]
                dispatch({
                    type: 'setSelectedSite',
                    payload: {
                        selectedSite
                    }
                })
            }
        }
    };
    return (<>
        <Graph
            graph={_graphData}
            options={options}
            events={events}
            getNetwork={network => {
                setNetwork(network)
                console.log(network)
                //  if you want access to vis.js network api you can set the state in a parent component using this property
            }}
        />
    </>);
}