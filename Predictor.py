import pickle
import os.path as path
import re

class Predictor(object):
    """Class for managing language models and NGram objects"""
    def __init__(self, language_files):
        self.training_data = [TrainData(**language) for language in language_files]

        self.build_models()

    def build_models(self):
        for train_data in self.training_data:
            train_data.build_ngrams()

    def predict(self, input_string):
        input_ngram = NGram(input_string, "input_string")

        best_match = input_ngram.find_match([train_data.ngram for train_data in self.training_data])
        return best_match

class TrainData(object):
    """Holds the training data and functions for checking if ngrams are up to date"""
    def __init__(self, language, training_file):
        self.language = language
        self.training_file = training_file
        self.ngram = None

    def build_ngrams(self):
        if self.is_stale():
            print("Rebuilding model for {} - {}".format(self.language, self.pickle_name()))

            with open(self.training_file, 'r') as f:
                self.ngram = NGram(f.read(), self.language)
                self.save_pickle()
        else:
            print("Loading model for {} - {}".format(self.language, self.pickle_name()))
            self.load_pickle()
            return self.ngram

    def load_pickle(self):
        with open(self.pickle_name(), 'rb') as pickle_file:
            self.ngram = pickle.load(pickle_file)

    def save_pickle(self):

        with open(self.pickle_name(), 'wb') as pickle_file:
            pickle.dump(self.ngram, pickle_file)

    def pickle_name(self):
        in_path, extension = path.splitext(self.training_file)
    
        pickle_filename = "{}_ngrams.txt".format(path.basename(in_path))
        return pickle_filename

    def is_stale(self):
        training_file_timestamp = path.getmtime(self.training_file)
        if not path.isfile(self.pickle_name()):
            return True
        else:
            return training_file_timestamp > path.getmtime(self.pickle_name())


class NGram(object):
    def __init__(self, text, language, n=3):
        self.length = None
        self.language = language
        self.n = n
        self.table = {}
        self.parse_text(text)
        self.calculate_length()

    def parse_text(self, text):
        # Strip Whitespace
        stripped_text = re.sub(r'\s+', ' ', text).strip()
        chars = ' ' * self.n # initial sequence of spaces with length n

        for letter in (" ".join(stripped_text.split()) + " "):
            chars = chars[1:] + letter # append letter to sequence of length n
            self.table[chars] = self.table.get(chars, 0) + 1 # increment count

    def calculate_length(self):
        """ Treat the N-Gram table as a vector and return its scalar magnitude
        to be used for performing a vector-based search.
        """
        self.length = sum([x * x for x in self.table.values()]) ** 0.5
        return self.length

    def __sub__(self, other):
        """ Find the difference between two NGram objects by finding the cosine
        of the angle between the two vector representations of the table of
        N-Grams. Return a float value between 0 and 1 where 0 indicates that
        the two NGrams are exactly the same.
        """
        if not isinstance(other, NGram):
            raise TypeError("Can't compare NGram with non-NGram object.")

        if self.n != other.n:
            raise TypeError("Can't compare NGram objects of different size.")

        total = 0
        for k in self.table:
            total += self.table[k] * other.table.get(k, 0)

        return 1.0 - (float(total) / (float(self.length) * float(other.length)))

    def find_match(self, languages):
        """ Out of a list of NGrams that represent individual languages, return
        the best match.
        """
        return min(languages, key=lambda ngram: self - ngram)
