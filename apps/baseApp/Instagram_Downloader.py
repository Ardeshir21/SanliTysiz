# -*- coding: utf-8 -*-
"""
Created on Sat May 22 15:50:22 2021

@author: Ardeshir Damavandi
"""

import requests
import re
import urllib.request


class crawler():
    def __init__(self, required_url):

        self.requesting_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36 Maxthon/5.3.8.2000',
                             'authority': 'www.instagram.com',
                             'method': 'GET',
                             'scheme': 'https',
                             'dnt': '1',
                             'upgrade-insecure-requests': '1',
                             'Origin': 'https://www.instagram.com',
                             'accept-encoding': 'gzip, deflate, br',
                             'accept-language': 'en-US',
                             'cache-control': 'max-age=0',
                             'sec-ch-ua-mobile': '?0',
                             'sec-fetch-dest': 'document',
                             'sec-fetch-mode': 'navigate',
                             'sec-fetch-site': 'none',
                             'sec-fetch-user': '?1',
                             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
                             }
        self.required_url = required_url

    # get the response Text
    def get_response_text(self, url):
        # Add Referer to the header
        r = requests.get(url, headers=self.requesting_header)
        if r.status_code != 200:
            print("Request is not possible")
            return None
        return r.text

    # change the recieved download link to make it usable
    def prepare_urls(self, matches):
        return list({match.replace("\\u0026", "&") for match in matches})

    # list the Videos or Images addresses in the rquired_url
    def list_media_addresses(self):
        response = self.get_response_text(self.required_url)

        vid_matches = re.findall('"video_url":"([^"]+)"', response)
        pic_matches = re.findall('"display_url":"([^"]+)"', response)

        vid_urls = self.prepare_urls(vid_matches)
        pic_urls = self.prepare_urls(pic_matches)

#        if vid_urls:
#            print('Detected Videos:\n{0}'.format('\n'.join(vid_urls)))
#
#        if pic_urls:
#            print('Detected Pictures:\n{0}'.format('\n'.join(pic_urls)))

        if not (vid_urls or pic_urls):
            print('Could not recognize the media in the provided URL.')
            return False

        return {'videos_addresses': vid_urls,
        'images_addresses': pic_urls}

#%%
#new_crawler = crawler('https://www.instagram.com/p/CO0uOVTj2c4/')
#new_crawler.list_media_addresses()
