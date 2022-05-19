#!/usr/bin/env python3
"""
This is designed to scrape books from flippingbooks.com and build them
into PDF's. This program requires internal modules flipbook_scraper,
and svg2pdf. Also requires external modules PyPDF2, reportlab, Request,
and svglib. Fonts need to be fixed to use what's embedded in the .svg,
and I should be able to get reportlab to replace PyPDF2.
> python3 ./flipbook2pdf.py -u <url> -d (directory)
See README.md for more information.
"""

import argparse
from pathlib import Path

import flipbook_scraper
import svg2pdf


def main(url,temp_dir):
    """ This is the main application flipbook2pdf """

    # Get the list of files to download.
    file_name,files = flipbook_scraper.book_info(url)
    print("Generated a list of files to download.")
    print("The book will be saved as {}.".format(file_name))

    # Download the files to the temp directory.
    print("Starting file downloads.")
    flipbook_scraper.download_files(files,temp_dir)
    print("File downloads are complete.")

    # Convert the .svg and .png files to .pdf files.
    print("Starting conversion to pdf's.")
    svg2pdf.svg_pdf(temp_dir)

    print("Bulding final {} in the current working directory".format(file_name))
    svg2pdf.merge_pdf(file_name,temp_dir)
    print("{} is complete.".format(file_name))

    return(0)


def get_args():
    """Gets url for the flippingbook, this can be the flippingbook.com
   website, or others such as a school website. An optional temporary
   directory can be provided where the working files will be written.
   The default temp directory is the current directory /temp/.
   """

    parser = argparse.ArgumentParser(description='Download a Flipbook.')
    parser.add_argument('-u','--url', dest='url', type=str, required=True, 
                        help='URL for the flipbook.')
    parser.add_argument('-d','--dir', dest='temp_dir', default='temp', type=Path, required=False, 
                        help='The temporary directory to download files to.')
    args = parser.parse_args()
    return(args.url,args.temp_dir)


if __name__ == "__main__":
    url,temp_dir = get_args()
    #Check if the temp directory exists already, and create it if not.
    if temp_dir.exists() is False:
        temp_dir.mkdir(parents = False, exist_ok = False)
        print("Temporary directory created at {}".format(str(temp_dir)))
    main(url,temp_dir)

