#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' 
This is designed to scrape books from flippingbooks.com and build them into PDF's
This program requires external modules PyPDF2, reportlab, and svglib.
This is a work in progress, and happens over multiple steps. 
Some things can be simplified, such as working on files instead of writing everything to disk, but this is left as a 
way to continue to build functionality for other uses. 
'''

from pathlib import Path
from PyPDF2 import PdfFileMerger, PdfFileReader
import re
from reportlab.graphics import renderPDF, renderPM
from reportlab.pdfgen import canvas
import requests
from svglib.svglib import svg2rlg


def book_info(url):
    '''Takes the URL to a flippingbook, pulls out information to download the files, and returns a list of files
    I'll be working to improve my web and java knowledge, and clean up this section in the future.'''
    
    #take the given URL, and find the flippingbook.com URL. 
    response = requests.get(url)
    content = response.content.decode()  
    flipping_book = re.findall(r'a href="(.*?flippingbook.*)/"',content)[0]
    
    response_two = requests.get(flipping_book)
    resp = response_two.content.decode()
    
    #to-do, return the file name for the pdf.
    #file_name = re.findall(r'PdfName":"(.*?)"',resp)[0]
    
    #Get the arguments needed to download the files
    path_prefix = re.findall(r'PathPrefix":"(.*?)"',resp)[1]
    policy = re.findall(r'Policy":"(.*?)"',resp)[1]
    signature = re.findall(r'Signature":"(.*?)"',resp)[1]
    key_id = re.findall(r'KeyId":"(.*?)"',resp)[1]
    renderer_version = re.findall(r'RendererVersion":"(.*?)"',resp)[0]
    number_pages = re.findall(r'TotalPages":(.*?)'',',resp)[0]

    #build the file paths based on the arguments.
    base_path = 'https' + path_prefix
    svg_path = 'common/pages/vector/' #to-do, get path from response, not hardcoded
    png_path = 'common/pages/html5substrates/page' #to-do, get path from response, not hardcoded
    post_path = '?Policy=' + policy + '&Signature=' + signature + '&Key-Pair-Id=' + key_id + '&uni=' + renderer_version
    

    all_files = file_list(base_path,svg_path,png_path,post_path,int(number_pages))
    return(all_files)

def file_list(base_path,svg_path,png_path,post_path,number_pages):
    '''Given the needed information, builds the list of files to download'''
    
    svg_ext = '.svg' #to-do, get extension from response, not hardcoded
    png_ext = '_1.webp' #to-do, get extension from response, not hardcoded
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
    '''Given a list of files and temp directory, it sets proper request headers and downloads all of the files''' 
    
    #to-do, figure out mandatory and optional headers.
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
    'Accept':'image/avif,image/webp,*/*',
    'Accept-Language':'en-US,en;q=0.5',
    'Accept-Encoding':'gzip, deflate, br',
    'Origin':'https://online.flippingbook.com',
    'DNT':'1',
    'Connection':'keep-alive',
    'Referer':'https://online.flippingbook.com/',
    'Sec-Fetch-Dest':'image',
    'Sec-Fetch-Mode':'cors',
    'Sec-Fetch-Site':'cross-site'}

    #writes all files to the temp_dir, using the key as the file name
    for i in all_files:
        for key,value in i.items():
            with open(str(temp_dir) +'/'+ key,'wb') as file:
                file_content = requests.get(value,headers = headers)
                file.write(file_content.content)
    print("Finished downloading all of the files.")
    
    #the requests library properly decoded the base64 .webp streaming content as .png, rename files accordingly.
    for old_name in (list(Path(temp_dir).glob('*.webp'))):
        new_name = str(old_name).replace('_1.webp','.png')
        old_name.rename(new_name)
    print("Renamed all of the *_1.webp files to .png")
    return()


def fix_font(font_data):
    '''Function to take the font data from the .svg files and write it to the path,
    then fix the svglib/reportlabs font issues'''


    return()

def fix_svg(file_base):
    '''This function pulls out the width, heigh, and font information from the .svg.
    It then inserts an image tag pointing to the .png file with the same name,
    this allows them to render properly as standalone .svg files.'''

    with open(file_base + '.svg','r+',encoding='utf-8') as svg_object:
        svg_data = svg_object.read()
        width_height = re.findall(r'width="(.*?)" height="(.*?)"',svg_data)[1]
        font_data = re.findall(r'@font-face {.*?}',svg_data)
        width = width_height[0]
        height = width_height[1]
        png_tag = '<svg:image href="{}.png" x="0" y="0" width="{}" height="{}" />'.format(file_base,width,height)
        svg_list = svg_data.split('<svg:defs>')
        svg_list.insert(1,png_tag + '<svg:defs>')
        svg_data = ''.join(svg_list)
        svg_object.seek(0)
        svg_object.write(svg_data)

    fix_font(font_data)
    return(width,height)

def svg_pdf(temp_dir):
    '''Given a directory with .svg and .png files, it converts the .svg files to individual .pdf files.
    if there is a .png with the same file name, it draws the .svg on top of the .png file'''
    
    svg_files =  list(Path(temp_dir).glob('*.svg'))

    for item in svg_files:
        base_file = str(item).removesuffix('.svg')
        width,height = fix_svg(base_file)

        #to-do, fix the font issues. Fonts are embedded in the .svg files.
        drawing = svg2rlg(item)
        my_canvas = canvas.Canvas(base_file + '.pdf')
        
        #to-do, get height, width from .svg instead of hard-coding.
        my_canvas.drawImage(base_file + '.png',0,0,width=width,height=height)         
        renderPDF.draw(drawing,my_canvas,0,0)
        my_canvas.save()
        
    return()

def merge_pdf(temp_dir):
    '''Merges all of the .pdf files in the give directory into a single file in the working directory'''

    mergedObject = PdfFileMerger()
    pdf_files =  list(Path(temp_dir).glob('*.pdf'))

    for file in pdf_files:
        mergedObject.append(PdfFileReader(str(file),'rb'))

    #to-do, get filename from the flipbook.
    mergedObject.write("mergedfilesoutput.pdf")


    return()

if __name__ == "__main__":
    
    #Change later to get inputs from users
    temp_dir = Path('temp')
    url = 'https://info.umbctraining.com/bookshelf-pp'
    
    #Check if the temp directory exists already, and create it if not.
    if temp_dir.exists() == False:
        temp_dir.mkdir(parents = False, exist_ok = False)
        print("Temporary directory created at {}".format(str(temp_dir)))
   
    #Get the list of files to download.
    files = book_info(url)
    print("Generated a list of files to download.")

    #Download the files to the temp directory.
    print("Starting file downloads.")
    download_files(files,temp_dir)
        
    #Convert the .svg and .png files to .pdf files. 
    svg_pdf(temp_dir)
    merge_pdf(temp_dir)