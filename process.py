#!/usr/bin/python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import sys
import re
import hashlib
from inc.models import *

import algorithm

def process(book):
    excerpt = get_random_part_of_text(book.text, 1000)
    #print excerpt
    words = get_words_for_string(excerpt)
    #print words

    """make statistical analysis"""
    genre = algorithm.bayes(words, 1)
    if genre != book.getCategoryId():
        algorithm.classify(words, 1, book.getCategoryId()) 
        print 0, book.getCategoryId(), len(words)
    else:
        print 1, book.getCategoryId()

    sys.stdout.flush()

def get_random_part_of_text(text, excerpt_length):
    text = re.sub(r'End of the Project Gutenberg EBook(?:.|\n)*', '', text, 1)
    text = re.sub(r'(?:.|\n)*?(\*+ START OF THIS PROJECT GUTENBERG EBOOK' + \
                  r'|with this eBook or online at www.gutenberg.(?:net|org)' + \
                  r'|\*END\*THE SMALL PRINT! FOR PUBLIC DOMAIN ETEXTS).*[\r\n]+' + \
                  r'(?:Produced by .*[\r\n]+|)', '', text, 1)

    length = len(text);
    import random
    start = random.randint(0, max(length-excerpt_length, 0))
    start = text.find('. ', start)+2
    if start < 0:
        start = 0
    end   = min(text.find('. ', start+excerpt_length), length)
    if end < 0:
        end = start + 1000 # could happen that a word is cut here, but thats not to much of a problem
    return text[start:end]

def get_words_for_string(text):
    text  = re.sub('^\W+|\W+$', '', text);
    words = re.split('\W+', text)
    return words

start = int(sys.argv[1])
for i in range(int(start),40000):
    book = BookRaw.objects.filter(book_raw_id=i)
    if book:
        print 'book ' + str(i)
        process(book[0])
