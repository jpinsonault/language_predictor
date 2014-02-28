import socket 
from glob import glob
from os.path import basename
from Predictor import Predictor

host = ''
port = 50000
backlog = 5
size = 1024

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))
    s.listen(backlog)
    predictor = Predictor(get_language_files())

    while True: 
        client, address = s.accept() 
        data = client.recv(size)
        print("Recieved {}".format(data))
        if data:
            ngram = predictor.predict(data)
            print("Sending {}".format(ngram.language_name))

            client.send(ngram.language_name)
        client.close()


def get_language_files():
    language_files = glob("C:\\Users\\joe\\Documents\\language_predictor\\*_language.txt")

    language_names = [language_from_path(path) for path in language_files]
    zipped = zip(language_names, language_files)

    language_dict = [{"language_name": line[0], "training_file": line[1]} for line in zipped]
    return language_dict


def language_from_path(path):
    filename = basename(path)
    return filename.split("_language")[0]


if __name__ == '__main__':
    main()