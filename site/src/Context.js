
import { createContext } from "react";
import React, { useState, useContext, useReducer } from "react";
import data from "./data.json"
import graph from "./graph.json"


const value = {
    domain: undefined,
    depath: 1,
}

let domainDataMap = {}
data.map(item => {
    let site = new URL(item.url)
    domainDataMap[site.hostname] = item
})


const computeGraph = (domain, depth = 2) => {

    // maxNodeNum 只对 graph  数据生效。
    let maxNodeNum = localStorage.getItem("maxNodeNum")
    if (!maxNodeNum) {
        maxNodeNum = data.length
        localStorage.setItem("maxNodeNum", maxNodeNum)
    }
    let pushedUrl = new Set()
    let graphData = {
        "nodes": [
        ],
        "edges": [
        ]
    }
    const addData2Graph = (domain, depth) => {
        let _depth = depth
        if (_depth > -1) {
            _depth--
            let site = domainDataMap[domain]
            let domainList = domain.split('.')
            let tld = domainList[domainList.length - 1]
            if (site && !pushedUrl.has(site.url)) {
                graphData.nodes.push({
                    "id": site.url,
                    "label": site.url,
                    "title": site.name,
                    "group": tld
                })
                pushedUrl.add(site.url)
                site.friends.map(link => {
                    try {
                        let u = new URL(link)
                        addData2Graph(u.hostname, _depth)
                    } catch (error) {
                        console.log(error)
                    }
                })
                let edges = site.friends.map(to => ({
                    from: site.url,
                    to: to
                }))
                graphData.edges = graphData.edges.concat(edges)
            }
        }
    }
    if (domain) {
        addData2Graph(domain, depth)
        return graphData
    } else {
        if (graph.nodes.length > maxNodeNum) {
            graph.nodes = graph.nodes.slice(0, maxNodeNum)
        }
        return graph
    }
}


const AppContext = createContext({})

const AppReducer = (state, action) => {
    switch (action.type) {
        case ('setDomain'):
            const { domain } = action.payload
            return {
                ...state,
                domain,
                graphData: computeGraph(domain, state.depath)
            }
        case 'clearCard':
            return {
                ...state,
                domain: undefined,
                selectedSite: undefined,
                graphData: computeGraph(undefined, state.depath)
            }
        case 'setSelectedSite':
            const { selectedSite } = action.payload
            return {
                ...state,
                domain: (new URL(selectedSite.url)).hostname,
                selectedSite
            }
        case 'set':
            return {
                ...state,
                ...action.payload
            }
        case 'computeGraph':
            return {
                ...state,
                graphData: computeGraph(state.domain, state.depath)
            }
        default:
            return state
    }
}

const AppContextProvider = (props) => {
    const [state, dispatch] = useReducer(AppReducer, value);

    return (
        <AppContext.Provider value={{ state, dispatch }}>
            {props.children}
        </AppContext.Provider>
    );
}

export { AppContext, AppContextProvider, domainDataMap };