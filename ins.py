import requests
import re
import json


def spider(n):
    proxies = {
        "http": "http://127.0.0.1:1087",
        "https": "http://127.0.0.1:1087",
    }
    url = 'https://www.instagram.com/'

    r = requests.get(url + n, proxies=proxies)
    a = re.findall("window._sharedData = (.+?);</script>", r.text)
    b = a[0]
    c = json.loads(b)
    print(c)

    biography = c['entry_data']['ProfilePage'][0]['graphql']['user']['biography']
    followers = c['entry_data']['ProfilePage'][0]['graphql']['user']['edge_follow']['count']
    follows = c['entry_data']['ProfilePage'][0]['graphql']['user']['edge_followed_by']['count']
    pics = c['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['count']
    name = c['entry_data']['ProfilePage'][0]['graphql']['user']['full_name']

    print(n)
    print("biography:")
    print(biography)
    print("followers:")
    print(followers)
    print("follows:")
    print(follows)
    print("pics:")
    print(pics)
    print("name:")
    print(name)


spider('joy.redvelvet')
