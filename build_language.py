import re
import argparse
import os
import json
from ngram_utils import build_ngrams
from ngram_utils import sanitize

args = None

def parse_args():
    global args

    parser = argparse.ArgumentParser()
    parser.add_argument('language_file')

    args = parser.parse_args()


def main():
    file_text = get_file(args.language_file)
    sanitized = sanitize(file_text)

    ngrams = build_ngrams(sanitized)
    
    save_ngrams(ngrams)


def save_ngrams(ngrams):
    in_path, extension = os.path.splitext(args.language_file)
    
    out_filename = "{}_ngrams.txt".format(os.path.basename(in_path))
    with open(out_filename, 'w') as out_file:
        out_file.write(json.dumps(ngrams))


def get_file(filename):
    with open(filename, 'r') as open_file:
        return open_file.read()


if __name__ == '__main__':
    parse_args()
    main()
