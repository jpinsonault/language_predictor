language_predictor
==================

Simple project I made for fun to build language models and predict what language a string or text file belongs to. It creates a model for each reference language, caching it to disk for repeated use, and rebuilds the model if the language file is updated.

I use the `NGram` class from [http://blog.ebookglue.com/write-language-detector-50-lines-python/](http://blog.ebookglue.com/write-language-detector-50-lines-python/), which I've modified slightly. Check it out for the theory as to why this predictor works. 

I've included some language files with text I got from Project Gutenberg

Included languages: chinese, dutch, english, french, german, japanese, latin, ancient-greek, modern-greek, polish, romanian, russian, spanish

To create a new language reference text, just slap any old text into a file and load it in (as described below). The only thing it does before building the language model is reduce all whitespace down to single spaces. It also has unicode support. 

One thing to note is that languages with a lot of diacritics (á, é, č, ć, đ, etc) might not perform well if you input a string without the marks, as it treats them as completely separate characters. For these languages make sure to construct the model file with text that includes the marks and text that doesn't have them, so the model has a variety to work with.

Using the `Predictor` Class
========
```python
from Predictor import Predictor
language_files = [
    {"language": "english", "training_file": "english_language.txt"},
    {"language": "spanish", "training_file": "spanish_language.txt"},
    {"language": "german", "training_file": "german_language.txt"},
]

predictor = Predictor(language_files)
best_guess = predictor.predict("Ich bin ein Berliner")

print("Language is: {}".format(best_guess.language))

# prints: Language is: german
```
`predict_language.py`
================
Or you can use the script I included, which takes a string or text file from the command line and guesses it's language. It loads all files of the format &lt;languagename&gt;_language.txt in the current directory and builds models for them

    usage: predict_language.py [-h] [-s STRING] [-f TEXT_FILE]
    
    optional arguments:
      -h, --help    show this help message and exit
      -s STRING
      -f TEXT_FILE

Example:

    $ predict_language.py -s "Fryderyk Franciszek Chopin polski kompozytor i pianista"
    Loading model for ancient-greek - ancient-greek_language_ngrams.txt
    Loading model for polish - polish_language_ngrams.txt
    .
    .
    .
    Loading model for spanish - spanish_language_ngrams.txt
    Language is: polish