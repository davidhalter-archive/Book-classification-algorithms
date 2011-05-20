#!/usr/bin/python
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import sys
import re
import hashlib
from inc.models import *
from Numeric import *
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
        #print 'wrong', book.category, len(words)
        stat[experiment_id][book.category][1] += 1
    else:
        #print 'right', book.category
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


books = int(sys.argv[1])
try:
    limit = int(sys.argv[2])
except IndexError:
    limit = 5000

stat_file = []
for i in range (0,6):
    stat_file.append({})
    for genre in ('detective', 'adventure', 'poetry'):
        stat_file[i][genre] = open('stat/%s_exp%i_stat_file.csv' % (genre, i),'a')

stat = {}
exp_stat = zeros((6,3))
experiments = ["bayes single words 1000",
               "bayes single words start 1000",
               "1  k_nearest_neighbor single words", 
               "3  k_nearest_neighbor single words", 
               "5  k_nearest_neighbor single words", 
               "10 k_nearest_neighbor single words", 
               ]
try:
    letter_count = int(sys.argv[3])
except IndexError:
    letter_count = 1000

iterations = 5
for n in range(0,iterations):
    print 'Durchlauf '+str(n+1)
    stat = {}
    adventure_count = 0;
    poetry_count = 0;
    detective_count = 0;

    i = 0;
    while(i < limit and (adventure_count < books or poetry_count < books or detective_count < books)):
        book = BookRaw.objects.filter(book_raw_id=i).exclude(category='children') \
                                                    .exclude(category='sf') \
                                                    .exclude(category='love') \
                                                    .exclude(category='fantasy') \
                                                    .exclude(category='comedies')
        if adventure_count >= books:
            book = book.exclude(category='adventure')
        if poetry_count >= books:
            book = book.exclude(category='poetry')
        if detective_count >= books:
            book = book.exclude(category='detective')                                        
        
        if book:
            if(book[0].category == 'adventure'):
                adventure_count+=1
            if(book[0].category == 'poetry'):
                poetry_count+=1
            if(book[0].category == 'detective'):
                detective_count+=1

            print 'book ' + str(i)
            train_on_error(book[0], 0, algorithm.bayes, get_words_single, letter_count)
            train_on_error(book[0], 1, algorithm.bayes, get_words_single_start, letter_count)
            train_on_error(book[0], 2, algorithm.k_nearest_neighbor, get_words_single, letter_count, k_nearest_neighbor=1)
            train_on_error(book[0], 3, algorithm.k_nearest_neighbor, get_words_single, letter_count, k_nearest_neighbor=3)
            train_on_error(book[0], 4, algorithm.k_nearest_neighbor, get_words_single, letter_count, k_nearest_neighbor=5)
            train_on_error(book[0], 5, algorithm.k_nearest_neighbor, get_words_single, letter_count, k_nearest_neighbor=10)
        i += 1

    exp_nr = 0
    for id, exp in stat.iteritems():
        cat_nr = 0        
        for cat, s in exp.iteritems():
            exp_stat[exp_nr][cat_nr] += s[0]
            cat_nr += 1
        exp_nr += 1
    print 'delete hash table...'
    Hash.objects.all().delete()

print "\n\nStatistical analysis:"
for id, exp in stat.iteritems():
    print "\nExperiment %d (%s):" % (id, experiments[id]) 
    q = 0
    for cat, s in exp.iteritems():
        right_count = exp_stat[id][q]
        wrong_count = books*iterations - right_count
        quote = float(right_count) / (books*iterations)
        print cat + ':\tright:\t'+str(right_count)+'\twrong:\t'+str(wrong_count)+'\tquote:\t'+str(quote)
        stat_file[id][cat].write('%d,%d\n' % (right_count, wrong_count))
        q += 1

# close statistic files
for i in range (0,6):
    for genre in ('detective', 'adventure', 'poetry'):
        stat_file[i][genre].close()   
 

