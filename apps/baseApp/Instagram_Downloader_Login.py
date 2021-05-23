# -*- coding: utf-8 -*-
"""
Created on Sat May 22 15:50:22 2021

@author: Ardeshir Damavandi
"""

import requests
import re
import os
import urllib.request
from datetime import datetime
from urllib.parse import urlparse
import json
import pickle
from django.conf import settings


class crawler():
    def __init__(self, username='cristiano.international',
                 password='@rdeshiR21!)'):
        self.clawer_token = 'https://api.proxycrawl.com/?token=TR9ra9jPRdm7fgmY_uv5Lw&url='
        self.username = username
        self.password = password
        self.link = 'https://www.instagram.com/'
        self.login_url = 'https://www.instagram.com/accounts/login/ajax/'
        self.is_logged_in =False
        self.current_cookies = None
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

    # Login to Instagram and get the login Response
    def insta_login(self):

        # Get a cookie from main page
        time = int(datetime.now().timestamp())
        response = requests.get(self.clawer_token + self.link, headers=self.requesting_header)
        csrf = response.cookies['csrftoken']

        # Data to login
        payload = {
            'username': self.username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{time}:{self.password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        # header for logging in
        login_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "x-csrftoken": csrf
        }

        login_response = requests.post(self.login_url, data=payload, headers=login_header)
        print(login_response)
        login_response_json = json.loads(login_response.text)
        print(login_response_json)

        # if successful
        if login_response_json["authenticated"]:
            # set logged in status to True
            self.is_logged_in = True
            self.current_cookies = login_response.cookies.get_dict()
        else:
            ("Autentication Failed!")



    # get the response Text
    def get_response_text(self, required_url):
            if self.is_logged_in:
                # Set the Header
                custom_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36 Maxthon/5.3.8.2000',
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
                                 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                                 'path': urlparse(required_url).path
                                 }

                temp_response = requests.post(required_url,
                                              headers=custom_header,
                                              cookies=self.current_cookies)
                return temp_response.text
            # not logged in
            else:
                print("You're not logged in")
                self.is_logged_in = False
                return False

    # change the recieved download link to make it usable
    def prepare_urls(self, matches):
        return list({match.replace("\\u0026", "&") for match in matches})

    # list the Videos or Images addresses in the rquired_url
    def list_media_addresses(self, required_url):
        response = self.get_response_text(required_url)

        if response:
            vid_matches = re.findall('"video_url":"([^"]+)"', response)
            pic_matches = re.findall('"display_url":"([^"]+)"', response)

            vid_urls = self.prepare_urls(vid_matches)
            pic_urls = self.prepare_urls(pic_matches)

            if vid_urls:
                print('Detected Videos:\n{0}'.format('\n'.join(vid_urls)))

            if pic_urls:
                print('Detected Pictures:\n{0}'.format('\n'.join(pic_urls)))


            if not (vid_urls or pic_urls):
                print('Could not recognize the media in the provided URL.')
                return False
            if (vid_urls or pic_urls):
                return {'videos_addresses': vid_urls,
                'images_addresses': pic_urls}
        else:
            print("A problem in response")

    def save_crawler(self):
        # Perform Login action with the Crawler
        self.insta_login()

        if self.is_logged_in:
            # Save the Crawler Object
            temp_file_path = os.path.join(settings.MEDIA_ROOT, 'Crawlers', 'crawler.pickle')
            crawler_obj = open(temp_file_path, 'wb')
            pickle.dump(self, crawler_obj)
