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
            with open('data/'+itemdir, 'r') as f:
                item = json.load(f)
                url_set.add(item['url'])
                data['nodes'].append({
                    'id': item['url'],
                    'label': item['url'],
                    'title': item['name'],
                    'group': item['url'].split(".")[-1]
                })
                url_friends_map[item['url']] = item['friends']

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
