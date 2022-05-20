#!/usr/bin/env python3
"""
This is designed to scrape PDF books from flippingbooks.com.
The .svg and .png files are saved to a temp directory.
Fonts need to be fixed to use what's embedded in the .svg.
External dependency on requests
"""

from pathlib import Path
import re
from urllib.request import urlopen

import requests


def main():
    """ Main function. Will be modified to allow calling the scraper as
    a standalone app
    """
    print("This is designed to scrape PDF books from flippingbooks.com.")
    return


def book_info(url):
    """ Takes the URL to a flippingbook, parses through the page,
    and returns a dictionary with the book information.
    """
    book_info={'given_url':url}

    # Take the given URL, and find the flippingbook.com URL.
    try:    
        with urlopen(url) as response:
            content = (response.read()).decode()
    except Exception as exception:
        print("Unable to get the contents of URL:",url)
        return(1)

    flipping_book = re.findall(r'href="(.*?flippingbook.com/view/.*?)"',content)[0]
    try:
        with urlopen(flipping_book) as response:
            resp = (response.read()).decode()
    except Exception as exception:
        print("Unable to get the contents of the flippingbook URL:",flipping_book)
        return(1)
    
    # Get the general book information.
    book_info['image'] = re.findall(r'<meta itemprop="image" content="(.*?)"/>', resp)[0]
    book_info['title'] = re.findall(r'<title>(.*?)</title>',resp)[0]
    book_info['primary_url'] = re.findall(r'<link rel="canonical" href="(.*?)"/>',resp)[0]
    book_info['file_name'] = re.findall(r'PdfName":"(.*?)"',resp)[0]

    # Get the arguments needed to determine the content to download.
    book_info['content_version'] = re.findall(r'contentVersion:\s\'(.*?)\'',resp)[0]
    book_info['base_path'] = re.findall(r'"ContentRoot":"(.*?)"',resp)[0]
    book_info['renderer_version'] = re.findall(r'RendererVersion":"(.*?)"',resp)[0]
    book_info['number_pages'] = re.findall(r'TotalPages":(.*?)'',',resp)[0]

    # Gets the access values for the content, not the customization files.
    access_values = re.findall(r'{"KeyId.*?'+book_info.get('content_version')+'.*?}',resp)[0]
    book_info['policy'] = re.findall(r'Policy":"(.*?)"',access_values)[0]
    book_info['signature'] = re.findall(r'Signature":"(.*?)"',access_values)[0]
    book_info['key_id'] = re.findall(r'KeyId":"(.*?)"',access_values)[0]
    book_info['post_path'] = ('?Policy=' + book_info.get('policy') 
                              + '&Signature=' + book_info.get('signature') 
                              + '&Key-Pair-Id=' + book_info.get('key_id') 
                              + '&uni=' + book_info.get('renderer_version'))

    # Define file path information.
    # To-do, get path from response, not hardcoded
    book_info['svg_path'] = 'common/pages/vector/'
    book_info['png_path'] = 'common/pages/html5substrates/page' 
    book_info['svg_ext'] = '.svg'
    book_info['png_ext'] = '_1.webp'
    
    return(book_info)


def file_list(book_info):
    """ Builds the list of files to download. """
    all_files = []
    for page_num in range(1,int(book_info.get('number_pages'))+1):
        page_num = format(page_num,'04d')
        svg_file = page_num + book_info.get('svg_ext')
        png_file = page_num + book_info.get('png_ext')
        full_svg_path = (book_info.get('base_path') + book_info.get('svg_path') 
                         + svg_file + book_info.get('post_path'))
        full_png_path = (book_info.get('base_path') + book_info.get('png_path') 
                         + png_file + book_info.get('post_path'))
        all_files.append({svg_file:full_svg_path})
        all_files.append({png_file:full_png_path})

    return(all_files)


def download_files(all_files,temp_dir):
    """ Given a list of files and temp directory,
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
                # To-do, get urllib Request to decode streams to remove requests module.
                #request = Request(value, headers = headers)
                #with urlopen(request, timeout = 10) as response:
                    #file_content = response.read()
    print("Finished downloading all of the files.")
    
    # The requests library properly decoded the .webp as .png, rename files accordingly.
    for old_name in (list(Path(temp_dir).glob('*.webp'))):
        new_name = str(old_name).replace('_1.webp','.png')
        old_name.rename(new_name)
    print("Renamed all of the *_1.webp files to .png")
    return

if __name__ == "__main__":
    main()
