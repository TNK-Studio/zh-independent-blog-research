import React from 'react';
import ReactEchartsCore from 'echarts-for-react/lib/core';
import { Typography } from '@material-ui/core';


import echarts from 'echarts/lib/echarts';
import 'echarts/lib/chart/line';
import 'echarts/lib/chart/pie';
import 'echarts/lib/chart/bar';
import 'echarts/lib/component/tooltip';
import 'echarts/lib/component/title';
import 'echarts/lib/component/legend';
import 'echarts/lib/component/legendScroll';

import rawData from '../data.json';


const DataSummary = () => {
    const num100 = (a, all) => (<span style={{ color: 'dodgerblue' }}>{`${(a / all * 100).toFixed(2)} %（${a}）`}</span>)
    let allSiteNum = rawData.length
    let siteNumHasRss = rawData.filter(item => item.rss.length > 0).length
    let siteWithHttps = rawData.filter(item => item.url.startsWith("https")).length
    let siteWithBlogDomain = rawData.filter(item => item.domain.split(".")[0] === "blog").length
    return (<>
        <Typography component='body1'>
            当前爬取站点数量: {allSiteNum}
            <br />
            其中 {num100(siteNumHasRss, allSiteNum)} 的站点提供了 RSS 订阅
            <br />
            {num100(siteWithHttps, allSiteNum)}  的站点启用了 HTTPS
            <br />
            {num100(siteWithBlogDomain, allSiteNum)}的站点使用 blog 作为博客站点的子域名
        </Typography>
    </>)
}

const Pie = (props) => {
    const { legendData, seriesData, seriesName, title } = props
    let data = {
        legendData,
        seriesData
    }
    let options = {
        title: {
            text: title,
            subtext: '',
            x: 'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br />{b} : {c} ({d}%)"
        },
        legend: {
            type: 'scroll',
            orient: 'vertical',
            right: 10,
            top: 20,
            bottom: 20,
            data: data.legendData,
            // selected: data.selected
        },
        series: [
            {
                name: seriesName,
                type: 'pie',
                radius: '55%',
                center: ['50%', '50%'],
                data: data.seriesData,
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    }
    return (<>
        <ReactEchartsCore
            // style={{ height: '95%' }}
            echarts={echarts}
            option={options}
            notMerge={true}
            lazyUpdate={true}
        // theme={"theme_name"}
        // opts={} 
        />
    </>)
}

const GeneratorPie = () => {
    let legendData = [
        'Jekyll',
        'Hexo',
        'Gatsby',
        'Nuxt',
        'Typecho',
        'Ghost',
        'Hugo',
        'WordPress',
        'unknown'
    ]
    let seriesData = []
    legendData.forEach(g => {
        let len = rawData.filter(item => item.generator.startsWith(g)).length
        if (len > 5) {
            seriesData.push({
                name: g,
                value: len
            })
        }
    })
    return (
        <Pie
            legendData={legendData}
            seriesData={seriesData}
            seriesName={"generator"}
            title={"博客生成器占比"}
        />
    )
}
const TldPie = () => {
    let _legendData = new Set(rawData.map(item => item.tld))
    let legendData = []
    let seriesData = []

    let other = 0
    Array.from(_legendData).forEach(tld => {
        let len = rawData.filter(item => item.tld === tld).length
        if (len > 10) {
            seriesData.push({
                name: tld,
                value: len
            })
            legendData.push(tld)
        } else {
            other++
        }
    })
    legendData.push('其它')
    seriesData.push({
        name: '其它',
        value: other
    })
    return (
        <Pie
            legendData={legendData}
            seriesData={seriesData}
            seriesName={"tld"}
            title={"博客顶级域名占比"}
        />
    )
}

const Report = () => {
    return (
        <div style={{ textAlign: 'center', maxWidth: 800, margin: '0 auto' }}>
            <DataSummary />
            <TldPie />
            <GeneratorPie />
        </div>
    )
}

export default Report