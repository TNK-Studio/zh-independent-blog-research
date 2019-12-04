
import os
import json
import pickle

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score


pkl_path = os.path.join(os.path.dirname(__file__), 'is_zh_i9t_blog.pkl')


def learn():
    df = pd.read_json('dataset.json')
    X = df.drop("name", axis=1)
    drops = ["domain", "rss", "generator", "friends",
             "url", "is_zh_i9t_blog", "tld", "sld"]
    for i in drops:
        X = X.drop(i, axis=1)

    y = df.is_zh_i9t_blog
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    clf = tree.DecisionTreeClassifier(max_depth=15)
    clf = clf.fit(X_train, y_train)
    print(accuracy_score(y_test, clf.predict(X_test)))
    joblib.dump(clf, pkl_path)
    return clf


def is_zh_i9t_blog(data):
    data = json.dumps([data])
    test_data = pd.read_json(data)

    if os.path.exists(pkl_path):
        clf = joblib.load(pkl_path)
    else:
        clf = learn()

    return bool(clf.predict(test_data)[0])


if __name__ == "__main__":
    data = {
        "has_archive": 0,
        "has_tag": 1,
        "has_category": 0,
        "has_about": 1,
        "has_theme": 1,
        "has_zh_text": 1,
        "has_blog_text": 1,
        "has_generator": 1,
        "has_rss": 1,
        "len_friends": 1
        # "tld": "com",
        # "sld": "1a23"
    }
    if not os.path.exists(pkl_path):
        learn()
    print(is_zh_i9t_blog(data))
