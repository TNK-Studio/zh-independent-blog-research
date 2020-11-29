# 中文独立博客调研[WIP]

scrapy 重构中...


抓取中文独立博客数据及其友链关系，绘制成可交互的关系图表。用于探索中文独立博客之间的关联，挖掘有意思的数据。

https://zh-independent-blog-research.netlify.com/

## 获取源码&安装依赖

+ python 3.7+
+ pipenv
+ node 10+
+ yarn

```shell
git clone https://github.com/TNK-Studio/zh-independent-blog-research.git
cd zh-independent-blog-research
pipenv install
cd site
yarn
```

## 项目结构

+ blog_finder 博客爬虫 scrapy 
+ is_site_a_zh_i9t_blog 判断站点是否是中文独立博客 （改进中）
+ site 展示关系图的前端站点 （暂停）

## 设计思路&Roadmap

更多的细节，参见：https://www.notion.so/55e54db856e343dd847dc207057ee751