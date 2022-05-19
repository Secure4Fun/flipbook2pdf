#!/usr/bin/env python3
"""
This is designed to scrape PDF books from flippingbooks.com.
The .svg and .png files are saved to a temp directory.
Fonts need to be fixed to use what's embedded in the .svg.
"""

from pathlib import Path
import re
from urllib.request import urlopen, Request

import requests


def main():
    print("This is designed to scrape PDF books from flippingbooks.com.")
    exit(0)


def book_info(url):
    """Takes the URL to a flippingbook, pulls out information to 
    download the files, and returns a list of files. 
    """
    # Take the given URL, and find the flippingbook.com URL. 
    with urlopen(url) as response:
        content = (response.read()).decode()  
    flipping_book = re.findall(r'href="(.*?flippingbook.*)/"',content)[0]
    with urlopen(flipping_book) as response:
        resp = (response.read()).decode()
    file_name = re.findall(r'PdfName":"(.*?)"',resp)[0]
    
    # Get the arguments needed to determine the content to download.
    content_version = re.findall(r'contentVersion:\s\'(.*?)\'',resp)[0]
    base_path = re.findall(r'"ContentRoot":"(.*?)"',resp)[0]
    renderer_version = re.findall(r'RendererVersion":"(.*?)"',resp)[0]
    number_pages = re.findall(r'TotalPages":(.*?)'',',resp)[0]
    
    # Gets dictionary (as string here) of the values for the content, not the customization files. 
    content_values = re.findall(r'{"KeyId.*?'+content_version+'.*?}',resp)[0]    
    policy = re.findall(r'Policy":"(.*?)"',content_values)[0]
    signature = re.findall(r'Signature":"(.*?)"',content_values)[0]
    key_id = re.findall(r'KeyId":"(.*?)"',content_values)[0]

    # Build the file paths based on the arguments.
    svg_path = 'common/pages/vector/'  # To-do, get path from response, not hardcoded
    png_path = 'common/pages/html5substrates/page'  # To-do, get path from response, not hardcoded
    post_path = '?Policy=' + policy + '&Signature=' + signature + '&Key-Pair-Id=' + key_id + '&uni=' + renderer_version
    all_files = file_list(base_path,svg_path,png_path,post_path,int(number_pages))
    return(file_name,all_files)


def file_list(base_path,svg_path,png_path,post_path,number_pages):
    """Builds the list of files to download."""
    svg_ext = '.svg'
    png_ext = '_1.webp'
    all_files = []
    for i in range(1,number_pages+1):
        svg_file = format(i,'04d') + svg_ext
        png_file = format(i,'04d') + png_ext
        full_svg_path = base_path + svg_path + svg_file + post_path
        full_png_path = base_path + png_path + png_file + post_path 
        all_files.append({svg_file:full_svg_path})
        all_files.append({png_file:full_png_path})
    return(all_files)


def download_files(all_files,temp_dir):
    """Given a list of files and temp directory, 
    it sets proper request headers and downloads all of the files.
    """
    # To-do, figure out mandatory and optional headers.
    headers = {'Accept':'image/avif,image/webp,*/*',
    'Accept-Language':'en-US,en;q=0.5',
    'Accept-Encoding':'gzip, deflate, br',
    'Origin':'https://online.flippingbook.com',
    'DNT':'1',
    'Connection':'keep-alive',
    'Referer':'https://online.flippingbook.com/',
    'Sec-Fetch-Dest':'image',
    'Sec-Fetch-Mode':'cors',
    'Sec-Fetch-Site':'cross-site',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
    }

    # Writes all files to the temp_dir, using the key as the file name.
    for i in all_files:
        for key,value in i.items():
            with open(str(temp_dir) +'/'+ key,'wb') as file:
                file_content = requests.get(value,headers = headers)
                file.write(file_content.content)
                # To-do, get urllib Request to decode svg stream to remove requests module.
                #request = Request(value, headers = headers)
                #with urlopen(request, timeout = 10) as response:
                    #file_content = response.read()                
    print("Finished downloading all of the files.")
    
    # The requests library properly decoded the .webp as .png, rename files accordingly.
    for old_name in (list(Path(temp_dir).glob('*.webp'))):
        new_name = str(old_name).replace('_1.webp','.png')
        old_name.rename(new_name)
    print("Renamed all of the *_1.webp files to .png")
    return()


if __name__ == "__main__":
    main()

