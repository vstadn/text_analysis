# Vitalii Stadnyk

from collections import OrderedDict # used for sorting dictionary
from operator import itemgetter # used for sorting dictionary
import argparse # used for parsing arguments
from timeit import default_timer as timer # used for timing
import urllib.request
import pylab as pl
import numpy as np

# This function trims off a string from both sides until it starts and ends with either digit or character.
# It returns a string in a specified format if it was successfully trimmed, otherwise it will return an empty string.
def format_string(word):
    while(True):
        word = str(word)
        # Checking if the last character of the word is either digit or character.
        if not word[0].isalpha() or not word[0].isdigit:
            if(len(word) > 1):
                word = word[1:]
            else:
                word = ''
                break
        # Checking if the last character of the word is either digit or character.
        if not word[-1].isalpha() or not word[-1].isdigit:
            if(len(word) > 1):
                word = word[:-1]
            else:
                word = ''
                break
        # Checking if both first and last elements are either digits or characters.
        if word[0].isalpha() and word[0].isdigit and word[-1].isalpha() and word[-1].isdigit:
            break
    return word

# This function finds the maximum length of the word that is in top 10 most common words from the text.
def find_max_word_length(dictionary):
    max_word_length = 0
    counter = 0
    for word in dictionary.keys():
        counter += 1
        if max_word_length < len(word):
            max_word_length = len(word)
        if counter == 10:
            break
    return max_word_length

# This function finds the maximum length of the word count that is in top 10 most common words from the text.
def find_max_count(dictionary):
    max_count = 0
    counter = 0
    for count in dictionary.values():
        counter += 1
        if max_count < count:
            max_count = count
        if counter == 10:
            break
    return max_count

# This function is used to generate historgam bars for individual word.
# It returns individual strings with histogram bar. This function is used for algorithm 1.
def histogram(max_stars_possible, max_count, count):
    number_of_stars = int((count * max_stars_possible)/max_count)
    return number_of_stars * "*"

# This function prints 10 most common words along with their counts and histogram bars.
# It uses function histogram() within itself. This function is used for algorithm 1.
def output_print(max_stars_possible,max_count):
    print("Most  Frequent")
    counter = 0
    for word, count in words_list.items():
        number_of_stars = histogram(max_stars_possible,max_count,count)
        indent = '{:<' + str(max_word_length)+ '}' + "  " + '{:>' + str(max_count_length) + '}' + " " + '{:<' + str(max_stars_possible) + '}';
        print(indent.format(word, count, number_of_stars))
        counter += 1
        if counter == 10:
            break

# Used for plotting
def plot(dictionary):
    plot_dict = OrderedDict(list(dictionary.items())[:10])
    X = np.arange(len(plot_dict))
    pl.bar(X, list(plot_dict.values()), align='center', width=0.5)
    pl.xticks(X, list(plot_dict.keys()))
    ymax = max(list(plot_dict.values())) + 1
    pl.ylim(0, ymax)
    pl.show()

# Parsing arguments from the command line.
def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, help="Input file that needs to be analyzed(required).", required=True)
    parser.add_argument("-s", "--stopwords", type=str, help="File with the list of stop words(optional).", required=False)
    help="Choose preferred algorithm. 1 - for slower approach. Any other value/blank/no argument for faster approach.",required=False)
    parser.add_argument("-u", "--url", type=str, help="URL or not", required=False)
    parser.add_argument("-p", "--plot", type=str, help="yes if you want to plot it", required=False)
    return parser.parse_args()

if __name__ == "__main__":
    args = parser()
    try:
        if args.url == "yes":
            url = urllib.request.urlopen(args.input)
            url_text = url.read()
            url_file = open('url_file.txt',"w")
            url_file.write(url_text.decode('utf-8'))
            file = open('url_file.txt', "r+")
        else:
            file = open(args.input, "r+")
    except IOError:
        print("Error handling Input/Output files. Check the correctness of specified files names.")
    # Check if file with the list of stop words is given. If not, set stop words to none.
    if args.stopwords:
        # Populating list with all the 'stop' words.
        banned_words = [line.rstrip('\n') for line in open(args.stopwords)]
    else:
        banned_words = []
    # Dictionary which will keep track of recorded words and their count.
    words_list={}
    # Populate dictionary with words from the text along with their counts.
    for word in file.read().split():
        word = format_string(word)
        word = word.lower()
        if word not in banned_words:
            if word not in words_list:
                words_list[word] = 1
            else:
                words_list[word] += 1
    # Sort dictionary by values (if two keys have the same values, sort those in alphabetical order).
    words_list = OrderedDict(sorted(words_list.items(),key=itemgetter(1,0),reverse = True))
    # Value for the maximum length of the line.
    line_length = 80
    # Space reserved for spacing in between words, counts and histogram bars.
    reserved_space = 3

    # Taking care of all the spacing details
    max_word_length = find_max_word_length(words_list)
    max_count = find_max_count(words_list)
    max_count_length = len(str(max_count))
    max_stars_possible = line_length - max_word_length - max_count_length - reserved_space

    start_time = timer()
    output_print(max_stars_possible,max_count)
    stop_time = timer()
    elapsed_time = stop_time - start_time
    print(str(elapsed_time) + "s  took for calculating individual histogram bars one at a time.")
    
    if args.plot == "yes":
        plot(words_list)

    file.close()
