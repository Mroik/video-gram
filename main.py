#!/bin/python
from requests import Session
from argparse import ArgumentParser
from json import loads as to_json
from uuid import uuid4
from html import unescape
from re import findall
import ffmpeg
from os import remove


def load_cookies(opts):
    with open(opts.c, "r") as fd:
        temp = fd.read()
        temp = to_json(temp)
        opts.cook = {}
        for cc in temp:
            opts.cook[cc["name"]] = cc["value"]


def set_shortcode(opts):
    temp = opts.url[8:]  # Assuming it starts with https://
    opts.shortcode = temp.split("/")[2]


def find_urls(data):
    def only_url(tag: str):
        start = tag.find(">")
        end = tag.find("<", start)
        return unescape(tag[start + 1:end])

    found = findall("<BaseURL .*>.*</BaseURL>", data)
    return list(map(only_url, found))


def generate_video(dash, sess):
    parsed = find_urls(dash)
    base = uuid4()
    with open(f"temp_{base}.mp4", "wb") as fd:
        fd.write(sess.get(parsed[0]).content)
    with open(f"temp_{base}.mp3", "wb") as fd:
        fd.write(sess.get(parsed[-1]).content)
    
    vid = ffmpeg.input(f"temp_{base}.mp4")
    aud = ffmpeg.input(f"temp_{base}.mp3")
    ffmpeg.output(vid, aud, f"{base}.mp4").run()
    remove(f"temp_{base}.mp4")
    remove(f"temp_{base}.mp3")


def main(opts):
    sess = Session()
    sess.get(opts.url)
    
    cookies = opts.cook
    
    headers = {
        'authority': 'www.instagram.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.8',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.instagram.com',
        'sec-ch-ua': '"Brave";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-ch-ua-platform-version': '"6.3.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-gpc': '1',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }
    
    data = {
        'fb_dtsg': 'NAcPrYSUpWHkA9KixRKazAVxM8SyIp2p07m5bKB13ymUUxVXUKCF-JA:17864642926059691:1683851979',
        'fb_api_caller_class': 'RelayModern',
        'variables': '{"shortcode": "' + opts.shortcode + '"}',
        'doc_id': '6129119620513740',
    }
    
    response = sess.post('https://www.instagram.com/api/graphql', cookies=cookies, headers=headers, data=data)
    data = response.json()

    dash = data["data"]["xdt_api__v1__media__shortcode__web_info"]["items"][0]["video_dash_manifest"]
    if dash is not None:
        generate_video(dash, sess)

    carous = data["data"]["xdt_api__v1__media__shortcode__web_info"]["items"][0]["carousel_media"]
    if carous is None:
        return
    for item in carous:
        if item["video_dash_manifest"] is not None:
            generate_video(item["video_dash_manifest"], sess)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-c", help="Cookie file", type=str, required=True)
    parser.add_argument("url", help="URL of a post/reel")

    opts = parser.parse_args()
    if opts.c:
        load_cookies(opts)
    set_shortcode(opts)

    main(opts)
