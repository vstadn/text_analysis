You can use file with words that you don't want to be taken into account while analyzing text (stop words option). 
Additionally, this code is capable of scraping file from url and analyzing it as well (url option).

usage: text_analysis.py [-h] -i INPUT [-s STOPWORDS] [-a ALGORITHM] [-u URL]
                        [-p PLOT]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input file that needs to be analyzed(required).
  -s STOPWORDS, --stopwords STOPWORDS
                        File with the list of stop words(optional).
  -u URL, --url URL     URL or not
  -p PLOT, --plot PLOT  yes if you want to plot it
