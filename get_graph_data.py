import os
import json


def to_json_data():
    data = []
    for itemdir in iter(os.listdir('data')):
        if itemdir.endswith('.json'):
            with open('data/'+itemdir, 'r') as f:
                data.append(json.load(f))

    with open('site/src/data.json', 'w') as f:
        json.dump(data, f)
    # return data


def to_graphql_data():
    data = {'nodes': [], 'edges': []}

    url_set = set()
    url_friends_map = {}
    for itemdir in iter(os.listdir('data')):
        if itemdir.endswith('.json'):
            try:
                with open('data/'+itemdir, 'r') as f:
                    item = json.load(f)
                    url_set.add(item['url'])
                    d = {
                        'id': item['url'],
                        'label': item['name'],  # 显示站点名称
                        'title': item['name'],
                        'group': item['url'].split(".")[-1],
                        # 'brokenImage':  "https://gine.me/icons/icon-48x48.png",
                    }

                    # fixme 默认加载的站点数量较多，显示 icon 会有大量的网络请求。
                    # if item['icon']:
                    #     d = {
                    #         **d,
                    #         'shape': "circularImage",
                    #         'image':  item['icon']
                    #     }

                    data['nodes'].append(d)
                    url_friends_map[item['url']] = item['friends']
            except Exception as e:
                print(e)
                print(item['url'])

    for url, friends in url_friends_map.items():
        for friend in friends:
            if friend in url_set:
                data['edges'].append({
                    'from': url,
                    "to": friend
                })

    with open('site/src/graph.json', 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    to_graphql_data()
    to_json_data()
