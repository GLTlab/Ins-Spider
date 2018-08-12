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


def r_get_image(X_Instagram_GIS, variables):
    my_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0',
        'X-Instagram-GIS': X_Instagram_GIS}
    url2 = 'https://www.instagram.com/graphql/query/?query_hash=bd0d6d184eefd4d0ce7036c11ae58ed9&variables=' + json.dumps(
        variables)
    r2 = requests.get(url2, headers=my_headers, proxies=proxies)
    a1 = json.loads(r2.text)

    return a1


def spider1(n):
    url = 'https://www.instagram.com/'
    my_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0'}
    r = requests.get(url + n, headers=my_headers, proxies=proxies)
    a = re.findall("window._sharedData = (.+?);</script>", r.text)
    b = a[0]
    c = json.loads(b)
    pics = c['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['count']
    id = c['entry_data']['ProfilePage'][0]['graphql']['user']['id']
    first = pics - 12
    after = c['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['page_info'][
        'end_cursor']
    rhx_gis = c['rhx_gis']
    # 获取信息 - 1
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
            url4 = c['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][i][
                'node'][
                'thumbnail_resources'][-1]['src']
            count = c['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][i][
                'node'][
                'edge_media_preview_like']['count']
            i = i + 1
            if (type1 != 'GraphImage'):
                continue
            list = []
            list.append(url4)
            list.append(count)
            print(list)
        else:
            break

    print("12 END")

    variables = {"user_id": id, "include_chaining": 'false', "include_reel": 'false',
                 "include_suggested_users": 'false', "include_logged_out_extras": 'true',
                 "include_highlight_reels": 'false'}
    gis = rhx_gis + ":" + json.dumps(variables)
    X_Instagram_GIS = hashlib.md5(gis.encode('utf-8')).hexdigest()
    my_headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0',
                  'X-Instagram-GIS': X_Instagram_GIS}
    url1 = 'https://www.instagram.com/graphql/query/?query_hash=7c16654f22c819fb63d1183034a5162f&variables=' + json.dumps(
        variables)
    r1 = requests.get(url1, headers=my_headers, proxies=proxies)
    print("Ver END")

    variables = {"id": id, "first": 12, "after": after}
    gis = rhx_gis + ":" + json.dumps(variables)
    X_Instagram_GIS = hashlib.md5(gis.encode('utf-8')).hexdigest()

    a1 = r_get_image(X_Instagram_GIS, variables)
    j = 0

    next = a1['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']

    #['entry_data']['ProfilePage'][0]['graphql']['user']['edge_media_collections']['page_info']['has_next_page']
    if (next == 'true'):
        next = 1
    else:
        next = 0
    while (next):
        my_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:62.0) Gecko/20100101 Firefox/62.0',
            'X-Instagram-GIS': X_Instagram_GIS}
        url2 = 'https://www.instagram.com/graphql/query/?query_hash=bd0d6d184eefd4d0ce7036c11ae58ed9&variables=' + json.dumps(
            variables)

        after =a1['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']['end_cursor']
        r2 = requests.get(url2, headers=my_headers, proxies=proxies)
        a1 = json.loads(r2.text)
        next = a1['data']['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
        if ((j + 11) < pics):
            type2 = a1['data']['user']['edge_owner_to_timeline_media']['edges'][j]['node']['__typename']
            if (type2 != 'GraphImage'):
                j = j + 1
                continue
            url3 = a1['data']['user']['edge_owner_to_timeline_media']['edges'][j]['node']['display_resources'][-1][
                'src']
            count1 = a1['data']['user']['edge_owner_to_timeline_media']['edges'][j]['node']['edge_media_preview_like'][
                'count']
            j = j + 1
            list1 = []
            list1.append(url3)
            list1.append(count1)
            print(list1)
        else:
            break


spider1('joy.redvelvet')
