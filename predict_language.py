import argparse
from glob import glob
from Predictor import Predictor

args = None

# Example language file configuraton that can be passed into Predictor's constructor
language_files = [
    {"language_name": "english", "training_file": "english_language.txt"},
    {"language_name": "spanish", "training_file": "spanish_language.txt"},
    {"language_name": "french", "training_file": "french_language.txt"},
    {"language_name": "german", "training_file": "german_language.txt"},
    {"language_name": "polish", "training_file": "polish_language.txt"},
    {"language_name": "romanian", "training_file": "romanian_language.txt"},
    {"language_name": "latin", "training_file": "latin_language.txt"},
]


def parse_args():
    global args

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='string')
    parser.add_argument('-f', dest="text_file")

    args = parser.parse_args()


def main():
    predictor = Predictor(get_language_files())
    best_guess = predictor.predict(get_input_string())

    print("Language is: {}".format(best_guess.language_name))

####################################################

def get_language_files():
    language_files = glob("*_language.txt")

    language_names = [filename.split("_language")[0] for filename in language_files]
    zipped = zip(language_names, language_files)

    language_dict = [{"language_name": line[0], "training_file": line[1]} for line in zipped]
    return language_dict



def get_input_string():
    if args.string:
        return args.string
    else:
        with open(args.text_file, 'r') as open_file:
            return open_file.read()


if __name__ == '__main__':
    parse_args()
    main()
