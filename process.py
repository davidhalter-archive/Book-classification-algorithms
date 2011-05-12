#!/usr/bin/python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import sys
import re
import hashlib
from inc.models import *

import algorithm

def train_on_error(book, experiment_id, algo, get_words, length, **kwargs):
    words = get_words(book, length)

    genre = algo(words, experiment_id, **kwargs)

    """make statistical analysis"""
    stat.setdefault(experiment_id, {})
    stat[experiment_id].setdefault(book.category, [0,0]) 

    if genre != book.getCategoryId():
        """ classifier is different for different algorithms """
        if algo == algorithm.bayes: 
            algorithm.classify(words, experiment_id, book.getCategoryId()) 
        else:
            algorithm.classify(words, experiment_id, book.book_raw_id) 
        print 'wrong', book.category, len(words)
        stat[experiment_id][book.category][1] += 1
    else:
        print 'right', book.category
        stat[experiment_id][book.category][0] += 1

    sys.stdout.flush()

def get_text_without_header(text):
    text = re.sub(r'End of the Project Gutenberg(?:.|\n)*', '', text, 1)
    text = re.sub(r'(?:.|\n)*?(\*+ START OF TH(?:IS|E) PROJECT GUTENBERG EBOOK' + \
                  r'|with this eBook or online at www.gutenberg.(?:net|org)' + \
                  r'|FOR COPYRIGHT PROTECTED ETEXTS\*END\*'+ \
                  r'|\nACT (?:I|1)|V\.12\.08\.93\]'+ \
                  r'|\*END\*? ?THE SMALL PRINT! FOR PUBLIC DOMAIN ETEXTS).*[\r\n]+' + \
                  r'(?:Produced by .*[\r\n]+|)', '', text, 1)

    #print text
    return text

def get_random_part_of_text(text, excerpt_length):
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
    text  = re.sub(r'^[\d\W_]+|[\d\W_]+$', '', text);
    words = re.split(r'[\d\W_]+', text)
    words = filter(lambda x: len(x) > 1, words)
    #words = map(lambda x: x.lower(), words)
    return words

def get_words_single(book, length):
    text = get_text_without_header(book.text)
    excerpt = get_random_part_of_text(book.text, length)
    #print excerpt
    words = get_words_for_string(excerpt)
    #print words
    return words

def get_words_single_start(book, length):
    text = get_text_without_header(book.text)[0:length]
    words = get_words_for_string(text)
    return words


start = int(sys.argv[1])
try:
    end = int(sys.argv[2])
except IndexError:
    end = start + 1

stat = {}
experiments = ["bayes single words 1000",
               "bayes single words start 1000",
               "1  k_nearest_neighbor single words", 
               "3  k_nearest_neighbor single words", 
               "5  k_nearest_neighbor single words", 
               "10 k_nearest_neighbor single words", 
               ]

for i in range(start, end):
    book = BookRaw.objects.filter(book_raw_id=i).exclude(category='children') \
                                                .exclude(category='sf') \
                                                .exclude(category='love') \
                                                .exclude(category='fantasy')
    if book:
        print '\nbook ' + str(i)
        train_on_error(book[0], 0, algorithm.bayes, get_words_single, 1000)
        train_on_error(book[0], 1, algorithm.bayes, get_words_single_start, 1000)
        train_on_error(book[0], 2, algorithm.k_nearest_neighbor, get_words_single, 1000, k_nearest_neighbor=1)
        train_on_error(book[0], 3, algorithm.k_nearest_neighbor, get_words_single, 1000, k_nearest_neighbor=3)
        train_on_error(book[0], 4, algorithm.k_nearest_neighbor, get_words_single, 1000, k_nearest_neighbor=5)
        train_on_error(book[0], 5, algorithm.k_nearest_neighbor, get_words_single, 1000, k_nearest_neighbor=10)

print "\n\nStatistical analysis:"
for id, exp in stat.iteritems():
    print "\nExperiment %d (%s):" % (id, experiments[id])
    for cat, s in exp.iteritems():
        print cat + ':\tright:\t', str(s[0]), '\twrong:\t', str(s[1])
    
