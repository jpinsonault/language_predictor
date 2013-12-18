import re

MIN_N = 2
MAX_N = 10

def sanitize(text):
    stripped = unicode(text, errors='ignore')
    # Strip all but letters and 
    stripped = re.sub(r'[().,;:<>?/\\{}"\'_0-9\-|+=\[\]!@#$%^&*]', '', stripped).strip()
    stripped = re.sub(r'\s+', ' ', stripped).strip()
    return stripped


def build_ngrams(text):
    word_list = ["${}_".format(word) for word in text.split()]

    ngrams_count = {}
    for word in word_list:
        for ngram in get_ngrams(word):
            ngrams_count[ngram] = ngrams_count.get(ngram, 0) + 1

    num_ngrams = len(ngrams_count)

    ngrams_percentage = {}

    for ngram, count, in ngrams_count.iteritems():
        ngrams_percentage[ngram] = count / float(num_ngrams)

    return ngrams_percentage 


def get_ngrams(word):
    n_tokens = len(word)
    for i in xrange(n_tokens):
        for j in xrange(i+MIN_N, min(n_tokens, i+MAX_N)+1):
            yield word[i:j]
