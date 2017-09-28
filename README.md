# GoogleImagesDownloader

Download images from google with specified keywords for searching

## Requirements

- python 3.5
- selenium 3.6.0
- Firefox
- geckodriver

Versions of FireFox and geckodriver should match, both of them are required by selenium

## Details and Configuration

Two types of downloading methods are provided

- `download_with_urllib`
- `download_with_selenium`


`download_with_urllib` is to download with just urllib, but due to the limit by google, each seaching query can download at most 100 images

`download_with_selenium` is to download with selenium and urllib, with selenium, we can directly search and scroll in the browser, so we can get more than 100 images for each searching query


Specify `main_keywords` and `supplemented_keywords` in the code, each main_keyword will join with each supplemented_keyword to become a searching query, and one directory will be created for each main_keyword to store the related images.

## Reference

https://github.com/atif93/google_image_downloader
https://github.com/hardikvasa/google-images-download