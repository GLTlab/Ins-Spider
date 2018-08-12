import requests
import re
import json
import sys
import hashlib

proxies = {
    "http": "http://127.0.0.1:1087",
    "https": "http://127.0.0.1:1087",
}


class safesub(dict):
    def __missing__(self, key):
        return '{' + key + '}'


def sub(text):
    return text.format_map(safesub(sys._getframe(1).f_locals))


#
# def r_get_image(X_Instagram_GIS, variables):
#     my_headers = {
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0',
#         'X-Instagram-GIS': X_Instagram_GIS}
#     url2 = 'https://www.instagram.com/graphql/query/?query_hash=bd0d6d184eefd4d0ce7036c11ae58ed9&variables=' + json.dumps(
#         variables)
#     r2 = requests.get(url2, headers=my_headers, proxies=proxies)
#     a1 = json.loads(r2.text)
#
#     return a1


def one(n):
    url = 'https://www.instagram.com/'
    my_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0'}
    r = requests.get(url + n, headers=my_headers, proxies=proxies)
    a = re.findall("window._sharedData = (.+?);</script>", r.text)
    b = a[0]
    c = json.loads(b)
    return c


def two(id, rhx_gis, after):
    variables = {"id": id, "first": 12, "after": after}
    gis = rhx_gis + ":" + json.dumps(variables)
    X_Instagram_GIS = hashlib.md5(gis.encode('utf-8')).hexdigest()
    my_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0',
                  'X-Instagram-GIS': X_Instagram_GIS}
    url2 = 'https://www.instagram.com/graphql/query/?query_hash=bd0d6d184eefd4d0ce7036c11ae58ed9&variables=' + json.dumps(
        variables)
    r2 = requests.get(url2, headers=my_headers, proxies=proxies)
    d = json.loads(r2.text)
    return d


def spider1(n):
    one(n)
    c = one(n)
    after = c['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info'][
        'end_cursor']
    rhx_gis = c['rhx_gis']
    id = c['entry_data']['ProfilePage'][0]['graphql']['user']['id']
    d = two(id, rhx_gis, after)
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
    i = 0
    while 1:
        if (i < 12):
            type1 = c['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][i][
                'node'][
                '__typename']
            url2 = c['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][i][
                'node'][
                'thumbnail_resources'][-1]['src']
            count = c['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][i][
                'node'][
                'edge_media_preview_like']['count']
            i = i + 1
            if (type1 != 'GraphImage'):
                continue
            list = []
            list.append(url2)
            list.append(count)
            print(list)
        else:
            break
    next = d['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
    j = 0
    while next:
        after_next = d['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
        d = two(id, rhx_gis, after_next)
        e = d['data']['user']['edge_owner_to_timeline_media']['edges']
        for j in e:
            type2 = j['node']['__typename']
            url3 = j['node']['display_resources'][-1]['src']
            count1 = j['node']['edge_media_preview_like']['count']
            if (type2 != 'GraphImage'):
                continue
            list1 = []
            list1.append(url3)
            list1.append(count1)
            print(list1)




spider1('al_gani.olshop')
