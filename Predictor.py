import sys
sys.path.append(r'C:\\Python27\\Lib')
sys.path.append(r'C:\\Users\\joe\\Documents\\language_predictor\\')
import pickle
import os.path as path
import re

class Predictor(object):
    """
        Predictor manages the task of building the language models and keeping
        them up to date 
    """
    def __init__(self, language_files):
        # **language unpacks to something like 
        #    {"language_name":"english", "training_file": "english_language.txt"}
        self.training_data = [TrainData(**language) for language in language_files]

        self.build_models()

    def build_models(self):
        for train_data in self.training_data:
            train_data.build_ngrams()

    def predict(self, input_string):
        """Compare an input string against all the stored models"""
        input_ngram = NGram(input_string, "input_string")

        best_match = input_ngram.find_match(train_data.ngram for train_data in self.training_data)
        return best_match


class TrainData(object):
    """TrainData objects manage the language model for a single language"""
    def __init__(self, language_name, training_file):
        self.language_name = language_name
        self.training_file = training_file

        self.ngram = None

    def build_ngrams_orig(self):
        """
            If there's a pickle for the model, we load it
            Otherwise build the model from scratch
        """
        if self.is_stale():
            print("Rebuilding model for {} - {}".format(self.language_name, self.pickle_name()))

            with open(self.training_file, 'r') as f:
                self.ngram = NGram(f.read(), self.language_name)
                self.save_pickle()
        else:
            print("Loading model for {} - {}".format(self.language_name, self.pickle_name()))
            self.load_pickle()
            return self.ngram

    def build_ngrams(self):
        """
            If there's a pickle for the model, we load it
            Otherwise build the model from scratch
        """
        with open(self.training_file, 'r') as f:
            self.ngram = NGram(f.read(), self.language_name)


    def load_pickle(self):
        with open(self.pickle_name(), 'rb') as pickle_file:
            self.ngram = pickle.load(pickle_file)

    def save_pickle(self):
        """We store the NGrams in pickles so they can be loaded quickly next time"""
        with open(self.pickle_name(), 'wb') as pickle_file:
            pickle.dump(self.ngram, pickle_file)

    def pickle_name(self):
        """
            Returns a filename to store the pickle in. 
            'filename.txt'->'filename_ngrams.txt'
        """
        in_path, extension = path.splitext(self.training_file)
    
        pickle_filename = "{}_ngrams.txt".format(path.basename(in_path))
        return pickle_filename

    def is_stale(self):
        """
            Returns True if the file doesn't exist or the language file is newer
            than the language model
        """
        training_file_timestamp = path.getmtime(self.training_file)
        if not path.isfile(self.pickle_name()):
            return True
        else:
            return training_file_timestamp > path.getmtime(self.pickle_name())


class NGram(object):
    """
        Creates and stores the NGram table
        Performs NGram comparisons
    """
    def __init__(self, text, language_name, n=3):
        self.length = None
        # Text 
        self.language_name = language_name
        self.n = n
        self.table = {}
        self.parse_text(text)
        self.calculate_length()

    def parse_text(self, text):
        """Creates a dictionary of n-grams and their counts"""
        # Strip Whitespace
        stripped_text = re.sub(r'\s+', ' ', text).strip()
        # initial sequence of spaces with length n
        chars = ' ' * self.n

        # This acts like a sliding window of width self.n 
        # moving across the input text
        for letter in (" ".join(stripped_text.split()) + " "):
            # append letter to sequence of length n
            chars = chars[1:] + letter
            # increment count
            self.table[chars] = self.table.get(chars, 0) + 1

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
