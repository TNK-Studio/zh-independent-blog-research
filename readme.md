# 中文独立博客调研

抓取中文独立博客数据及其友链关系，绘制成可交互的关系图表。用于探索中文独立博客之间的关系，挖掘有意思的数据。

![图的一部分](./assets/piece_of_graph.jpg)

## 依赖

+ pipenv
+ python 3.7+
+ npm
+ yarn

```shell
pipenv install
```

## 运行 

+ 抓取数据
    ```shell
    pipenv run app.py
    ```

+ 合成图数据 > site/src/data.json
    ```shell
    python get_graph.py
    ```

+ 构建前端

    ```
    cd site && yarn 
    yarn start # 开发
    yarn build # 构建
    yarn serve # 本地查看部署的站点（build 后）
    ```