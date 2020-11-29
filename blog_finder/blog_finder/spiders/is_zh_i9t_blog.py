import os
import json
import pickle

import pandas as pd
import joblib


pkl_path = os.path.join(os.path.dirname(__file__), 'is_zh_i9t_blog.pkl')


def is_zh_i9t_blog(data):
    print(data)
    data = json.dumps([data])
    test_data = pd.read_json(data)
    clf = joblib.load(pkl_path)
    res = bool(clf.predict(test_data)[0])
    return res


if __name__ == "__main__":
    data = {
        "has_archive": 0,
        "has_tag": 0,
        "has_category": 0,
        "has_about": 0,
        "has_theme": 0,
        "has_zh_text": 0,
        "has_blog_text": 0,
        "has_generator": 0,
        "has_rss": 0,
        "len_friends": 1000,        
        # "tld": "com",
        # "sld": "1a23"
    }
    print(is_zh_i9t_blog(data))
