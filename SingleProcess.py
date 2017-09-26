# -*- coding: utf-8 -*-
# @Author: lc
# @Date:   2017-09-25 23:54:24
# @Last Modified by:   lc
# @Last Modified time: 2017-09-26 21:49:38

import os
import time
import re
import logging
import urllib.request
import urllib.error


from user_agent import generate_user_agent


log_file = 'download.log'
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode="a+", format="%(asctime)-15s %(levelname)-8s  %(message)s")


def download_page(url):
    """download raw content of the page
    
    Args:
        url (str): url of the page 
    
    Returns:
        raw content of the page
    """
    try:
        headers = {}
        headers['User-Agent'] = generate_user_agent()
        headers['Referer'] = 'https://www.google.com'
        req = urllib.request.Request(url, headers = headers)
        resp = urllib.request.urlopen(req)
        return str(resp.read())
    except Exception as e:
        print('error while downloading page {0}'.format(url))
        logging.error('error while downloading page {0}'.format(url))
        return None


def parse_page(url):
    """parge the page and get all the links of images, max number is 100  due to limit by google
    
    Args:
        url (str): url of the page
    
    Returns:
        A set containing the urls of images
    """
    page_content = download_page(url)
    if page_content:
        link_list = re.findall('"ou":"(.*?)"', page_content)
        if len(link_list) == 0:
            print('get 0 links from page {0}'.format(url))
            logging.info('get 0 links from page {0}'.format(url))
            return set()
        else:
            return set(link_list)
    else:
        return set()


def download_images(main_keywords, supplemented_keywords):
    start_time = time.time()   #start the timer
    for i in range(len(main_keywords)):
        image_links = set()
        print('Main keyword: {0}'.format(main_keywords[i]))

        # create a directory for a main keyword
        img_dir = './data/{0}/'.format(main_keywords[i])
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)

        for j in range(len(supplemented_keywords)):
            print('supplemented keyword: {0}'.format(supplemented_keywords[j]))
            search_query = (main_keywords[i] + ' ' + supplemented_keywords[j]).replace(' ','%20')
            # url = 'https://www.google.com/search?q=' + search_query + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
            url = 'https://www.google.com/search?q=' + search_query + '&source=lnms&tbm=isch'
            image_links = image_links.union(parse_page(url))
            print('get {0} links so far'.format(len(image_links)))
            time.sleep(2)
        print ("Total Image Links: {0}".format(len(image_links)))
        print("Total time taken for getting all links: {0}s\n".format(time.time() - start_time))
        

        print ("Start downloading...")
        count = 1
        for link in image_links:
            try:
                req = urllib.request.Request(link, headers = {"User-Agent": generate_user_agent()})
                response = urllib.request.urlopen(req)
                data = response.read()
                file_path = img_dir + '{0}.jpg'.format(count)
                with open(file_path,'wb') as wf:
                    wf.write(data)
                print("Already download {0} images".format(count))
                count += 1
            except urllib.error.URLError as e:
                logging.error('URLError while downloading image {0}\nreason:{1}'.format(link, e.reason))
                continue
            except urllib.error.HTTPError as e:
                logging.error('HTTPError while downloading image {0}\nhttp code {1}, reason:{2}'.format(link, e.code, e.reason))
                continue
            except Exception as e:
                logging.error('Unexpeted error while downloading image {0}\nerror type:{1}, args:{2}'.format(link, type(e), e.args))
                continue

    print("Finish downloading, total {0} errors".format(len(image_links) - count))
    


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

    download_images(main_keywords, supplemented_keywords)