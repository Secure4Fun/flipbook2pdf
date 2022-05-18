# flipbook_scraper
This is designed to scrape books from flippingbooks.com and build them into PDF's. 
This is meant for your own use, on books you have permission to download.
This program requires external dependencies PyPDF2, reportlab, requests, and svglib. I plan to remove PyPDF2.
Fonts need to be fixed to use what's embedded in the .svg, and I should be able to get reportlab to replace PyPDF2.

Tested using Python 3.9, other versions should be fine as well.
Virtual environment is included in the package, and I will be moving some functions to classes later.
> git clone https://github.com/Secure4Fun/flipbook_scraper.git
> cd flipbook_scraper
> source env/Scripts/activate
> python3 ./flipbook_scraper.py -u <url> -d (directory)

Note: -d (directory) is optional. It will default to 'temp' inside of the current working directory.
Note: The final pdf will be saved as in the current working direcotry, as the pdf name from the flipbook.

If you just download the python script:
	On Linux run:
		'python3 -m pip install -r ./requirements.txt'
		'python3 ./flipbook_scraper.py'

	On Windows run:
		'py.exe -3 -m pip install -r .\requirements.txt'
		'py.exe -3 .\flipbook_scraper.py'