#!/usr/bin/env python3
"""
This module is to convert .svg's to a .pdf document.
Fonts need to be fixed to use what's embedded in the .svg.
"""

import argparse
from pathlib import Path
import re

from PyPDF2 import PdfFileMerger, PdfFileReader
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg


def main(args):
    """ Main function for the module. Plan to turn it into a stand-alone
   for svg to pdf converstion. Requires redefining functions.
   """
    print("This module is to convert .svg's to a .pdf document")
    print(args)
    return


def get_args():
    """ Parses the commandline input for running standalone. """
    parser = argparse.ArgumentParser(
        description = 'Converts SVG files to PDF files. You must speicfy the path to an existing'
        'file or directory. You can optionally specify  a temporary working directory, otherwise'
        '"<current directory>/temp" will be used.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-f', '--file', type=Path,
                        help='Path to a single SVG file to convert.')
    group.add_argument('-d', '--dir', type=Path, 
                        help='Path to a directory of SVG files to convert.')
    parser.add_argument('-t', '--temp', type=Path, default = 'temp', nargs='?',
                        help='Path to a temporary working directory.')
    args = parser.parse_args()
    
    if (args.file != None) and (Path.exists(args.file) == False):
        exit(f'The file {args.file} does not exist.')
    if (args.dir != None) and (Path.exists(args.dir) == False):
        exit(f'The directory {args.dir} does not exist.')
    return(args)


def fix_font(font_data):
    """ To-do, function to take the font data from the .svg files and write it to the path,
    then fix the svglib/reportlabs font issues.
    """
    return


def fix_svg(temp_dir,file_base):
    """ To-do, This function pulls out the width, height, and font information
    from the .svg. It then inserts an image tag pointing to the .png
    file with the same name, this allows them to render properly as
    standalone .svg files.
    """

    #setting default width and height in cases where the below fails.
    width = 612
    height = 792

    try:
        with open(file_base + '.svg','r+',encoding='utf-8') as svg_object:
            svg_data = svg_object.read()
            width_height = re.findall(r'rect.*?width="(.*?)" height="(.*?)".*?rect',svg_data)[0]
            font_data = re.findall(r'@font-face {.*?}',svg_data)
            width = width_height[0]
            height = width_height[1]
            file_name = file_base.removeprefix(str(temp_dir)+'\\')
            png_tag = '<svg:image href="{}.png" x="0" y="0" width="{}" height="{}" />'.format(
                file_name,width,height)
            svg_list = svg_data.split('<svg:defs>')
            svg_list.insert(1,png_tag + '<svg:defs>')
            svg_data = ''.join(svg_list)
            svg_object.seek(0)
            svg_object.write(svg_data)
    except Exception as exception:
        print(f'Failed to open {file_base}.svg and get width/height/font information.',
              exception)

    # To-do, fix the fonts.
    #fix_font(font_data)
    return(int(width),int(height))


def svg_pdf(temp_dir):
    """ Given a directory with .svg and .png files, it converts the .svg
    files to individual .pdf files. If there is a .png with the same
    file name, it draws the .svg on top of the .png file.
    """
    svg_files =  list(Path(temp_dir).glob('*.svg'))

    for item in svg_files:
        base_file = str(item).removesuffix('.svg')
        width,height = fix_svg(temp_dir,base_file)

        # To-do, fix the font issues. Fonts are embedded in the .svg files.
        drawing = svg2rlg(item)
        my_canvas = canvas.Canvas(base_file + '.pdf')
        my_canvas.drawImage(base_file + '.png',0,0,width=width,height=height)         
        renderPDF.draw(drawing,my_canvas,0,0)
        my_canvas.save()
    return()


def merge_pdf(file_name,temp_dir):
    """ To-do, Merges all of the .pdf files in the give directory into a single
    file in the working directory.
    """
    merged_object = PdfFileMerger()
    pdf_files =  list(Path(temp_dir).glob('*.pdf'))
    for file in pdf_files:
        merged_object.append(PdfFileReader(str(file),'rb'))
    merged_object.write(file_name)
    return()


if __name__ == "__main__":
    args = get_args()
    main(args)
