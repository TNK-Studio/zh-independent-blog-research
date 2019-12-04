
import { createContext } from "react";
import React, { useReducer } from "react";
import data from "./data.json"
import graph from "./graph.json"

let domainDataMap = {}
let blogSearcher = {}
data.forEach(item => {
    domainDataMap[item.domain] = item
    blogSearcher[item.domain] = JSON.stringify(item)
})


const value = {
    domain: undefined,
    depath: 1,
    q: undefined,
    blogList: []
}


const queryBlog = (q) => {
    let searchRes = Object.entries(blogSearcher).filter(item => {
        let [key, value] = item
        let qRegExp = new RegExp(q, 'i')
        // 全局正则搜索
        return value.search(qRegExp) > -1
    }).map(item => {
        let [key, value] = item
        return domainDataMap[key]
    })
    let r = searchRes.slice(0, 10)
    console.log(r)
    return r
}

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
                let nodeData = {
                    "id": site.url,
                    "label": site.name,
                    "title": site.name,
                    "group": tld
                }

                if (pushedUrl.size < 30) {
                    //  同屏节点少于 30 时，显示站点 icon
                    nodeData = {
                        ...nodeData,
                        'shape': "circularImage",
                        'image': site.icon,
                        'brokenImage': '/favicon.ico'
                    }
                }

                graphData.nodes.push(nodeData)
                pushedUrl.add(site.url)
                site.friends.forEach(link => {
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
        case 'setQ':
            const { q } = action.payload
            let blogList = queryBlog(q)
            if (blogList.length === 1) {
                let site = blogList[0]
                return {
                    ...state,
                    domain: site.domain,
                    selectedSite: site
                }
            } else {
                return {
                    ...state,
                    q,
                    blogList,
                    selectedSite: undefined
                }
            }

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
                q: undefined,
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