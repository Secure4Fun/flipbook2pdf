# flipbook2pdf.py
This is designed to convert books from flippingbooks.com and build them into PDF's.  
If you have a link with an embedded flippingbook this works as well. 
I do not have access to any that require passwords, so those are unsupported for now.
This is meant for your own use, on books you have permission to download, and is in no way officially affiliated with flippingbooks.com.
This program depends on PyPDF2, reportlab, requests, and svglib.
Fonts need to be fixed to use what's embedded in the .svg, work in progress on that. 

Tested using Python 3.9, other versions should be fine as well.  
Virtual environment is included in the package.

	> git clone https://github.com/Secure4Fun/flipbook2pdf.git   
	> cd flipbook2pdf  
	> source env/Scripts/activate  
	> python3 ./flipbook2pdf.py -u <url> -d (directory)  

Note: -d (directory) is optional. It will default to 'temp' in the current working directory.  
Note: The final pdf will be saved as in the current working direcotry,
as the pdf name from the flipbook.  

# full_site.py
This is for the data hoarders out there.  
It takes the sitemap for flippingbook, and writes out a text file of all public books.  
Then it sends the books from the file to flipbook_scraper, and writes a CSV file of their
basic information.    
Functionality will be added to read in a previous book list and update the list and CSV based on
differences between them.  

# svg2pdf.py
This relies heavily on svglib and reportlabs. I take no real credit here, just including it to 
clean up some things with flippingbook files, convert, and put it all together.  
Working to make it a standalone tool as well.  
