# -*- coding: utf-8 -*-
"""
Created on Sat May 22 15:50:22 2021

@author: Ardeshir Damavandi
"""

import requests
import re
from urllib.parse import quote_plus, urlparse
from django.conf import settings
from urllib.request import urlretrieve
import os


class crawler():
    def __init__(self, required_url):

        self.token= 'https://api.proxycrawl.com/?token=TR9ra9jPRdm7fgmY_uv5Lw'
        self.required_url = quote_plus(required_url)

    # get the response Text
    def get_response_text(self):
        # Add Referer to the header
        r = requests.get(self.token + '&url=' + self.required_url)
        if r.status_code != 200:
            print("Request is not possible")
            return None
        return r.text

    # change the recieved download link to make it usable
    def prepare_urls(self, matches):
        return list({match.replace("\\u0026", "&") for match in matches})

    # list the Videos or Images addresses in the rquired_url
    def list_media_addresses(self):
        response = self.get_response_text()

        vid_matches = re.findall('"video_url":"([^"]+)"', response)
        pic_matches = re.findall('"display_url":"([^"]+)"', response)

        vid_urls = self.prepare_urls(vid_matches)
        pic_urls = self.prepare_urls(pic_matches)

        # if vid_urls:
        #     print('Detected Videos:\n{0}'.format('\n'.join(vid_urls)))
        #
        # if pic_urls:
        #     print('Detected Pictures:\n{0}'.format('\n'.join(pic_urls)))

        if not (vid_urls or pic_urls):
            print('Could not recognize the media in the provided URL.')
            return False

        return {'videos_addresses': vid_urls,
        'images_addresses': pic_urls}

#%%
# new_crawler = crawler('https://www.instagram.com/p/COixLOLjUbF/')
# new_crawler.list_media_addresses()


# # if no crawler object exist, make one instance
# requested_url = 'https://www.instagram.com/p/COixLOLjUbF/'
# new_crawler = crawler(requested_url)
# media_addresses = new_crawler.list_media_addresses()
# videos_list = []
# images_list = []
#
# # Download all the files into the Server
# url_path = urlparse(requested_url).path
# url_path = url_path.replace('/', '_')
#
#
# # Vidoes
# for index, file in enumerate(media_addresses['videos_addresses'], start=1):
#     file_name = '{}_{}.mp4'.format(url_path, index)
#     temp_file_path = os.path.join('/home/ardeshir/SanliTysiz/media/', 'Downloads', file_name)
#     urlretrieve(file)
#     # add file name to the list
#     videos_list.append(file_name)
# # Images
# for index, file in enumerate(media_addresses['images_addresses'], start=1):
#     file_name = '{}_{}.jpg'.format(url_path, index)
#     temp_file_path = os.path.join('/home/ardeshir/SanliTysiz/media/', 'Downloads', file_name)
#     urlretrieve(file, temp_file_path)
#     # add file name to the list
#     images_list.append(file_name)
