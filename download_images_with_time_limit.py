# -*- coding: utf-8 -*-
# @Author: LC
# @Date:   2017-09-30 09:13:43
# @Last Modified by:   LC
# @Last Modified time: 2017-09-30 16:52:08

###########################################################################################################
# download images with time limit 
# bacause the method "download_images" in script "download_with_selenium.py" always block due to network issue
# and this file is a replacement of the method "download_images" 
# Pay attention that time-limited strategy is to use the signal that system provides
# and here the SIGALRM in unix-like system is adopted, so this script should run within unix-like system
###########################################################################################################

import os
import time
import signal
import logging
import urllib.request
import urllib.error
from urllib.parse import urlparse
from multiprocessing import Pool

from user_agent import generate_user_agent


class TimeLimitError(Exception):
    def __init__(self, value):
        Exception.__init__()
        self.value = value

    def __str__(self):
        return self.value


def handler(signum, frame):
    raise TimeLimitError('Time limit exceeded')


def download_with_time_limit(link_file_path, download_dir, log_dir, limit_time = 10):
    main_keyword = link_file_path.split('/')[-1]
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = log_dir + 'download_selenium_{0}.log'.format(main_keyword)
    logging.basicConfig(level = logging.DEBUG, filename = log_file, filemode = "a+", format = "%(asctime)-15s %(levelname)-8s  %(message)s")
    img_dir = download_dir + main_keyword + '/'
    count = 0
    headers = {}
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    signal.signal(signal.SIGALRM, handler)
    with open(link_file_path, 'r') as rf:
        for link in rf:
            try:
                ref = 'https://www.google.com'
                o = urlparse(link)
                ref = o.scheme + '://' + o.hostname
                ua = generate_user_agent()
                headers['User-Agent'] = ua
                headers['referer'] = ref

                # limit the time of downloading a image
                try:
                    signal.alarm(limit_time) # set a timeout(alarm)
                    req = urllib.request.Request(link.strip(), headers = headers)
                    response = urllib.request.urlopen(req)
                    data = response.read()
                except TimeLimitError as e:
                    print('TimeLimitError: process-{0} encounters {1}'.format(main_keyword, e.value))
                    logging.error('TimeLimitError while downloading image{0}'.format(link))
                    continue
                finally:
                    signal.alarm(0) # disable the alarm

                file_path = img_dir + '{0}.jpg'.format(count)
                with open(file_path,'wb') as wf:
                    wf.write(data)
                print('Process-{0} download image {1}/{2}.jpg'.format(main_keyword, main_keyword, count))
                count += 1
                if count % 10 == 0:
                    print('Process-{0} is sleeping'.format(main_keyword))
                    time.sleep(5)
            except urllib.error.HTTPError as e:
                print('HTTPError')
                logging.error('HTTPError while downloading image {0}http code {1}, reason:{2}'.format(link, e.code, e.reason))
                continue
            except urllib.error.URLError as e:
                print('URLError')
                logging.error('URLError while downloading image {0}reason:{1}'.format(link, e.reason))
                continue
            except Exception as e:
                print('Unexpected Error')
                logging.error('Unexpeted error while downloading image {0}error type:{1}, args:{2}'.format(link, type(e), e.args))
                continue


if __name__ == '__main__':
    main_keywords = ['neutral', 'angry', 'surprise', 'disgust', 'fear', 'happy', 'sad']

    supplemented_keywords = ['facial expression',\
                'human face',\
                'face',\
                'old face',\
                'young face',\
                'adult face',\
                'child face',\
                'woman face',\
                'man face',\
                'male face',\
                'female face',\
                'gentleman face',\
                'lady face',\
                'boy face',\
                'girl face',\
                'American face',\
                'Chinese face',\
                'Korean face',\
                'Japanese face',\
                'actor face',\
                'actress face'\
                'doctor face',\
                'movie face'
                ]

    download_dir = './data_limit_time/'
    link_files_dir = './data/link_files/'
    log_dir = './logs_limit_time/'

    """
    # single process
    for keyword in main_keywords:
        link_file_path = link_files_dir + keyword
        download_with_time_limit(link_file_path, download_dir)
    """
    # multiple processes
    p = Pool() # default number of process is the number of cores of your CPU, change it by yourself
    for keyword in main_keywords:
        p.apply_async(download_with_time_limit, args=(link_files_dir + keyword, download_dir, log_dir))
    p.close()
    p.join()
    print('Finish downloading all images')
