import re
import argparse
import os
import json
from glob import glob
from pprint import pprint
from ngram_utils import build_ngrams
from Predictor import Predictor
from Predictor import NGram

args = None

language_files = [
    {"language": "english", "training_file": "english_language.txt"},
    {"language": "spanish", "training_file": "spanish_language.txt"},
    {"language": "french", "training_file": "french_language.txt"},
    {"language": "german", "training_file": "german_language.txt"},
    {"language": "polish", "training_file": "polish_language.txt"},
    {"language": "romanian", "training_file": "romanian_language.txt"},
    {"language": "latin", "training_file": "latin_language.txt"},
]


def parse_args():
    global args

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='string')
    parser.add_argument('-f', dest="text_file")

    args = parser.parse_args()


def main():
    # print(get_language_files())
    predictor = Predictor(get_language_files())
    best_guess = predictor.predict(get_input_string())

    print(best_guess.language)


def get_language_files():
    language_files = glob("*_language.txt")

    language_names = [filename.split("_language")[0] for filename in language_files]
    zipped = zip(language_names, language_files)

    language_dict = [{"language": line[0], "training_file": line[1]} for line in zipped]
    return language_dict

####################################################
def old_main():
    language_ngrams = load_all_ngrams()
    
    input_ngrams = build_ngrams(get_input_string())

    scores = {}
    for language, ngram_data in language_ngrams.iteritems():
        scores[language] = get_score(input_ngrams, ngram_data)

    best_guess = max(scores.iterkeys(), key=(lambda key: scores[key]))

    total_percentage = sum(scores.values())
    score_ratios = {language:score/total_percentage for language, score in scores.items()}

    for language, score in score_ratios.items():
        print("{}: {:.0%}".format(language, score))

    print("Best guess is: {}".format(best_guess))


def get_input_string():
    if args.string:
        return args.string
    else:
        with open(args.text_file, 'r') as open_file:
            return open_file.read()


def get_score(input_ngrams, reference_ngrams):
    total = 0.0

    for ngram in input_ngrams:
        total += reference_ngrams.get(ngram, 0.0)

    return total


def load_all_ngrams():
    ngram_files = glob("*_ngrams.txt")

    ngrams = {}
    for ngram_file in ngram_files:
        language = ngram_file.split("_")[0]

        with open(ngram_file, 'r') as json_file:
            ngram_data = json.load(json_file)

        ngrams[language] = ngram_data

    return ngrams


if __name__ == '__main__':
    parse_args()
    main()
