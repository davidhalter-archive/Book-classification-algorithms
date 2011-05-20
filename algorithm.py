import hashlib
import operator

from inc.models import *
import category

""" worte klassifizieren """
def classify(words, experiment_id, class_id):
    for word in words:
        hash = hashlib.md5(word).hexdigest()
        h = Hash.objects.filter(experiment_id=experiment_id, hash=hash, class_id=class_id)
        if h:
            h = h[0]
            h.count = h.count + 1
        else:
            h = Hash(hash=hash,
                     experiment_id=experiment_id,
                     class_id=class_id,
                     count=1,
                     text=word)
        h.save()

def bayes(words, experiment_id, **kwargs):
    result = -1
    probabillity = {};
    wordCount = len(words)
    for word in words:
        h = hashlib.md5(word).hexdigest()
        tests = Hash.objects.filter(experiment_id=experiment_id, hash=h)
        temp = map(lambda obj: obj.count, tests) # get only the counts in a list
        count = reduce(lambda x,y: x+y, temp, 0)    # add all of them
        if count:
            for test in tests:
                # make calculation here
                # Vorkommnis in Kategorie X / (Vorkomnisse in allen Kategorien * Wortanzahl)
                # print count, test.count, wordCount
                calc = test.count/float(count*wordCount)
                try:
                    probabillity[test.class_id] += calc
                except KeyError:
                    probabillity.setdefault(test.class_id, calc) 
                    #probabillity[test.class_id] = 0#test.count/count
    #print probabillity;
    sort = sorted(probabillity.iteritems(), key=operator.itemgetter(1), reverse=True)
    #for i in range(0, min(3, len(probabillity))):
        #print category.get_category_for_id(sort[i][0]) + ':', '%.3f' % sort[i][1]
        
    if probabillity:
        result = max(probabillity, key=probabillity.get)
    return result

def k_nearest_neighbor(words, experiment_id, **kwargs):
    nearest = {}
    for word in words:
        h = hashlib.md5(word).hexdigest()
        tests = Hash.objects.filter(experiment_id=experiment_id, hash=h)
        for test in tests:
            try:
                nearest[test.class_id] += test.count
            except KeyError:
                nearest.setdefault(test.class_id, test.count) 

    sort = sorted(nearest.iteritems(), key=operator.itemgetter(1), reverse=True)
    #for i in range(0, min(kwargs['k_nearest_neighbor'], len(probabillity))):
    #print sort[0:kwargs['k_nearest_neighbor']]
    return k_nearest_neighbor_get_class(sort[0:kwargs['k_nearest_neighbor']])

def k_nearest_neighbor_get_class(nearest):
    if not len(nearest):
        return -1

    # is recursive!
    categories = {}
    for n in nearest:
        c_id = BookRaw.objects.filter(book_raw_id=n[0])[0].getCategoryId()
        try:
            categories[c_id] += 1
        except KeyError:
            categories[c_id] = 1

    maximum = max(categories.iteritems(), key=operator.itemgetter(1))
    count = 0
    for cat, cat_max in categories.iteritems():
        if cat_max == maximum[1]:
            count += 1
    #count = filter(lambda cat,cat_max: cat_max == maximum[1], categories.iteritems())
    #print maximum[1], categories, count
    if count > 1:
        result = k_nearest_neighbor_get_class(nearest[:len(nearest)-1])
    else:
        result = maximum[0]
    return result
    
