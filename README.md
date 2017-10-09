# GoogleImagesDownloader

Download images from google with specified keywords for searching

## Requirements

- python 3.5
- selenium 3.6.0
- Firefox
- geckodriver

Versions of FireFox and geckodriver should match, both of them are required by selenium

## Details and Configuration

Two different methods are provided

- `download_with_urllib`
- `download_with_selenium`


`download_with_urllib` is to download with just package `urllib`, but due to the limit by google, each searching query can download at most 100 images

`download_with_selenium` is to download with package `selenium` and `urllib`, with selenium, we can directly search and scroll in the browser, so we can get more than 100 images for each searching query

Specify `main_keywords` and `supplemented_keywords` in the code, each `main_keyword` will join with each `supplemented_keyword` to become a searching query, and one directory will be created for each main_keyword to store the related images.

As to the script `download_images_with_time_limit.py`, it is a replacement of the method `download_images` in script `download_with_selenium.py`, because the method `download_images` will always block due to network issue, so I add restriction that each http request can cost at most 10 sceonds, and that is what `download_images_with_time_limit.py` does. 

Pay attention that the time-limited strategy is to use the signal that system provides, and here the `SIGALRM` in unix-like system is adopted, so this script should run with unix-like system rather than Windows. However, the network blocking thing happened when I ran the script in my network, but not sure whether this will happen in yours, so you can test with `download_with_selenium.py` firstly, if the downloading task blocks, change to the script `download_images_with_time_limit.py`

More details about the repository can be obtained in [this blog](http://wulc.me/2017/09/23/Google%20%E5%9B%BE%E7%89%87%E7%88%AC%E8%99%AB/)

## Reference

- https://github.com/atif93/google_image_downloader
- https://github.com/hardikvasa/google-images-download