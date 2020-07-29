"""
@file:bli_download.py
@time:2020/7/26-17:36
@api方式下载视频
"""
import re

import requests

from utils.general_config import headers


class BiliBili:
    def __init__(self):
        self.api_page_list = "https://api.bilibili.com/x/player/pagelist?bvid=%s"
        self.api_video_list = "https://api.bilibili.com/x/player/playurl?cid={}&qn={}&bvid={}"

    @staticmethod
    def get_request_result(url):
        html = requests.get(url, headers=headers, timeout=60).json()
        data = html['data']
        return data

    def get_video_list(self, bvid, quality=80):
        start_url = self.api_page_list % bvid
        data = self.get_request_result(start_url)
        videoList = list()
        for item in data:
            cid = str(item['cid'])
            title = item['part']
            title = re.sub(r'[\/\\:*?"<>|]', '', title)  # 替换为空的
            page = item['page']
            refer_url1 = "%s?p=%s" % (start_url, page)
            video_list = self.get_play_list(start_url, cid, quality, bvid)

            onevideo = {'title': title, 'video_url': video_list[0], 'page': page, 'refer_url': refer_url1}

            videoList.append(onevideo)
        return videoList

    def get_play_list(self, refer_url, cid, quality, bvid):
        url_api = self.api_video_list.format(cid, quality, bvid)
        headers['Referer'] = refer_url  # 注意加上referer
        html = requests.get(url_api, headers=headers, timeout=120).json()
        video_list = [i['url'] for i in html['data']['durl']]
        return video_list

    def down_video(self):
        pass


if __name__ == '__main__':
    bvid = "BV1Qt41147GV"
    bili = BiliBili()
    bili.get_video_list(bvid)
