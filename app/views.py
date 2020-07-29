import urllib.request
from urllib.parse import quote

import requests
from flask import render_template, request, Response

from app import app, bl_download


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/getVideoList', methods=['GET'])
def getVideoList():
    bv = request.args.get('bv')
    # 视频质量
    quality = request.args.get("quality")
    videolist = bl_download.get_video_list(bv, quality)
    return render_template("videolist.html", videolist=videolist)


@app.route('/download_video', methods=['POST', 'GET'])
def download_video():
    # data = request.get_json()
    # 获取数据并转化成字典
    info = request.form.to_dict()
    refer_url = info.get('refer_url')
    video_download_url = info.get('video_download_url')
    title = info.get('title')
    print(f"获取完毕:{refer_url}")
    opener = urllib.request.build_opener()
    # 请求头
    opener.addheaders = [
        ('Host', 'upos-hz-mirrorks3.acgvideo.com'),  # 注意修改host,不用也行
        ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
        ('Accept', '*/*'),
        ('Accept-Language', 'en-US,en;q=0.5'),
        ('Accept-Encoding', 'gzip, deflate, br'),
        ('Range', 'bytes=0-'),  # Range 的值要为 bytes=0- 才能下载完整视频
        ('Referer', refer_url),  # 注意修改referer,必须要加的!
        ('Origin', 'https://www.bilibili.com'),
        ('Connection', 'keep-alive'),
    ]
    urllib.request.install_opener(opener)
    print("开始请求！")
    try:
        print(type(video_download_url))
        res = urllib.request.urlopen(url=video_download_url)
    except Exception as err:
        print(err)
        return "error"
    print("请求完毕！")
    response = Response(file_iterator(res), content_type='application/octet-stream')
    print("迭代完毕！")
    response.headers["Content-disposition"] = 'attachment; filename={0}; filename*=utf-8''{0}'.format(
        quote(title) + '.flv')
    print("处理完毕！")

    return response


@app.route('/text', methods=['GET'])
def file_download():
    """
    文件下载测试
    :return:
    """
    def send_chunk():
        with open('111.flv', 'rb') as target_file:  # 读取文件内容
            while True:
                chunk = target_file.read(20 * 1024 * 1024)
                if not chunk:
                    break
                yield chunk

    response = Response(send_chunk(), content_type='application/octet-stream')  # 响应指明类型，写入内容
    response.headers["Content-disposition"] = 'attachment; filename={0}; filename*=utf-8''{0}'.format('1111.flv')
    return response


def file_iterator(f):
    chunk_size = 20000  # 每次读取的片大小
    while True:
        c = f.read(chunk_size)
        if c:
            yield c
        else:
            break
