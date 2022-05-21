#!/usr/bin/env python3
"""
This module is being developed to scrape the sitemap files.
It writes out a small csv with basic book information.
It will be able to update the document listings on a recurring basis.
"""

import csv
from lxml import etree
from urllib import request

import flipbook_scraper


def get_url(url):
    """ Gets the content of the URL """
    try:
        with request.urlopen(url) as site:
            content = site.read()
    except Exception as exception:
        print("Unable to get the contents of URL:",url)
        retun(1)    
    return(content)

def parse_sitemap(url):
    """ Builds the sitemap for flippingbook, and returns a list of 
    dict of sites with books.
    """
    site_maps = {}    
    content = get_url(url)
    root = etree.fromstring(content)
    
    for sitemap in root:
        site_maps[(sitemap.getchildren()[0].text)] = ''

    print("Got the list of sitemaps, now getting the list of books.")

    for site in site_maps:
        books = []
        content = get_url(site)
        root = etree.fromstring(content)
        for book in root:
            books.append(book.getchildren()[0].text)
        site_maps[site] = books
    
    print(f'Got the list of {len(books)} books.')
    return(site_map)

def book_list(file_name):
    """ Reads the book file in, sends URL's to write the CSV of data. 
    To-do, Reads in a file, and compares it to the current book file.
    To-do, Gets the diff in the lists, and appends them to the file.
    """
    
    with open(file_name,'r') as book_file:
        book_urls = book_file.readlines()

    for book_url in book_urls:
        site_csv(book_url.strip())
    return

def site_csv(book_url):
    """ Takes the book URL and appends basic info to a CSV file. """
    # To-do, use csv.Dictwriter to simplify and incorporate headers.
    # To-do, allow users to specify file name.
    try:
        book_info = flipbook_scraper.book_info(book_url)
    except Exception as exception:
        print("Failed to get book info from flipbook_scraper for:", book_url)
        return
    try:
        row = (book_info.get('title'), book_info.get('file_name'), book_info.get('number_pages'),
               book_info.get('primary_url'),book_info.get('password'))
    except Exception as exception:
        print("Failed to properly parse out book info for:", book_url)
   
    try:
        with open('books.csv','a',newline='',encoding = 'utf-8') as csv_file:
            writer = csv.writer(csv_file, dialect='excel')
            writer.writerow(row)
    except Exception as exception:
        print("Failed to write book info for:", book_url)
    return

if __name__ == "__main__":

    sitemap_url = 'https://online.flippingbook.com/sitemap/sitemap.xml'
    books = parse_sitemap(sitemap_url)
   
    book_file = 'book_list.txt'
    book_list(book_file)

    #books_str = '\n'.join(books)
    #with open('book_list.txt','wt') as book_list:
    #    book_list.write(books_str)
