# 中文独立博客调研

抓取中文独立博客数据及其友链关系，绘制成可交互的关系图表。用于探索中文独立博客之间的关联，挖掘有意思的数据。

https://zh-independent-blog-research.netlify.com/

![图的一部分](./assets/piece_of_graph.jpg)

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

## 运行 

+ 抓取数据
    ```shell
    pipenv run app.py
    ```

+ 合成图数据 > site/src/data.json
    ```shell
    python get_graph_data.py
    ```

+ 构建前端

    ```
    cd site # site 目录下
    yarn start # 运行开发服务器
    yarn build # 构建生产版本
    yarn serve # 本地查看部署的站点（build 后）
    ```

## 说明

项目初始阶段为了验证想法，希望依赖尽可能的少。没有引入 redis、数据库等组件。采用单机多进程+协程的方式爬取数据。采用文件系统存储数据。
如果因意外情况崩溃，可以使用下如下命令恢复运行状态，继续爬取。

+ 获取未完成的队列 & 清理数据
```
python clean_data.py
```