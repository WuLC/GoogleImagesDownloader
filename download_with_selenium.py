# -*- coding: utf-8 -*-
# @Author: WuLC
# @Date:   2017-09-27 23:02:19
# @Last Modified by:   LC
# @Last Modified time: 2017-09-30 10:54:36


####################################################################################################################
# Download images from google with specified keywords for searching
# search query is created by "main_keyword + supplemented_keyword"
# if there are multiple keywords, each main_keyword will join with each supplemented_keyword
# Use selenium and urllib, and each search query will download any number of images that google provide
# allow single process or multiple processes for downloading
# Pay attention that since selenium is used, geckodriver and firefox browser is required
####################################################################################################################

import os
import json
import time
import logging
import urllib.request
import urllib.error
from urllib.parse import urlparse

from multiprocessing import Pool
from user_agent import generate_user_agent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_image_links(main_keyword, supplemented_keywords, link_file_path, num_requested = 1000):
    """get image links with selenium
    
    Args:
        main_keyword (str): main keyword
        supplemented_keywords (list[str]): list of supplemented keywords
        link_file_path (str): path of the file to store the links
        num_requested (int, optional): maximum number of images to download
    
    Returns:
        None
    """
    number_of_scrolls = int(num_requested / 400) + 1 
    # number_of_scrolls * 400 images will be opened in the browser

    img_urls = set()
    driver = webdriver.Firefox()
    for i in range(len(supplemented_keywords)):
        search_query = main_keyword + ' ' + supplemented_keywords[i]
        url = "https://www.google.com/search?q="+search_query+"&source=lnms&tbm=isch"
        driver.get(url)
        
        for _ in range(number_of_scrolls):
            for __ in range(10):
                # multiple scrolls needed to show all 400 images
                driver.execute_script("window.scrollBy(0, 1000000)")
                time.sleep(2)
            # to load next 400 images
            time.sleep(5)
            try:
                driver.find_element_by_xpath("//input[@value='Show more results']").click()
            except Exception as e:
                print("Process-{0} reach the end of page or get the maximum number of requested images".format(main_keyword))
                break

        # imges = driver.find_elements_by_xpath('//div[@class="rg_meta"]') # not working anymore
        imges = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
        for img in imges:
            img_url = json.loads(img.get_attribute('innerHTML'))["ou"]
            # img_type = json.loads(img.get_attribute('innerHTML'))["ity"]
            img_urls.add(img_url)
        print('Process-{0} add keyword {1} , got {2} image urls so far'.format(main_keyword, supplemented_keywords[i], len(img_urls)))
    print('Process-{0} totally get {1} images'.format(main_keyword, len(img_urls)))
    driver.quit()

    with open(link_file_path, 'w') as wf:
        for url in img_urls:
            wf.write(url +'\n')
    print('Store all the links in file {0}'.format(link_file_path))


def download_images(link_file_path, download_dir, log_dir):
    """download images whose links are in the link file
    
    Args:
        link_file_path (str): path of file containing links of images
        download_dir (str): directory to store the downloaded images
    
    Returns:
        None
    """
    print('Start downloading with link file {0}..........'.format(link_file_path))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    main_keyword = link_file_path.split('/')[-1]
    log_file = log_dir + 'download_selenium_{0}.log'.format(main_keyword)
    logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode="a+", format="%(asctime)-15s %(levelname)-8s  %(message)s")
    img_dir = download_dir + main_keyword + '/'
    count = 0
    headers = {}
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    # start to download images
    with open(link_file_path, 'r') as rf:
        for link in rf:
            try:
                o = urlparse(link)
                ref = o.scheme + '://' + o.hostname
                #ref = 'https://www.google.com'
                ua = generate_user_agent()
                headers['User-Agent'] = ua
                headers['referer'] = ref
                print('\n{0}\n{1}\n{2}'.format(link.strip(), ref, ua))
                req = urllib.request.Request(link.strip(), headers = headers)
                response = urllib.request.urlopen(req)
                data = response.read()
                file_path = img_dir + '{0}.jpg'.format(count)
                with open(file_path,'wb') as wf:
                    wf.write(data)
                print('Process-{0} download image {1}/{2}.jpg'.format(main_keyword, main_keyword, count))
                count += 1
                if count % 10 == 0:
                    print('Process-{0} is sleeping'.format(main_keyword))
                    time.sleep(5)

            except urllib.error.URLError as e:
                print('URLError')
                logging.error('URLError while downloading image {0}reason:{1}'.format(link, e.reason))
                continue
            except urllib.error.HTTPError as e:
                print('HTTPError')
                logging.error('HTTPError while downloading image {0}http code {1}, reason:{2}'.format(link, e.code, e.reason))
                continue
            except Exception as e:
                print('Unexpected Error')
                logging.error('Unexpeted error while downloading image {0}error type:{1}, args:{2}'.format(link, type(e), e.args))
                continue


if __name__ == "__main__":
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

    download_dir = './data/'
    link_files_dir = './data/link_files/'
    log_dir = './logs/'

    ###################################
    # get image links and store in file
    ###################################
    """
    # single process
    for keyword in main_keywords:
        link_file_path = link_files_dir + keyword
        get_image_links(keyword, supplemented_keywords, link_file_path)
    

    # multiple processes
    p = Pool(3) # default number of process is the number of cores of your CPU, change it by yourself
    for keyword in main_keywords:
        p.apply_async(get_image_links, args=(keyword, supplemented_keywords, link_files_dir + keyword))
    p.close()
    p.join()
    print('Fininsh getting all image links')
    """
    ###################################
    # download images with link file
    ###################################
    """
    # single process
    for keyword in main_keywords:
        link_file_path = link_files_dir + keyword
        download_images(link_file_path, download_dir)
    """
    # multiple processes
    p = Pool() # default number of process is the number of cores of your CPU, change it by yourself
    for keyword in main_keywords:
        p.apply_async(download_images, args=(link_files_dir + keyword, download_dir, log_dir))
    p.close()
    p.join()
    print('Finish downloading all images')
    