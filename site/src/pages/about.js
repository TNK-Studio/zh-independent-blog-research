import React from 'react';
import { Typography } from '@material-ui/core';


const About = () => {
    return (
        <div style={{ maxWidth: 800, margin: '0 auto', padding: '2em' }}>
            <Typography>
                目前项目以验证想法为主，不会爬取太多数据。
                <br />
                完成下列事项后，开始批量爬取数据。
                <ul>
                    <li>完善：搜索</li>
                    <li>优化：站点是否是中文独立博客的验证方法</li>
                </ul>
                <br />
                项目地址 GitHub:<a href="https://github.com/TNK-Studio/zh-independent-blog-research"> https://github.com/TNK-Studio/zh-independent-blog-research </a>

            </Typography>
        </div>
    )
}

export default About