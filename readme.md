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
yarn start 
yarn build 
```