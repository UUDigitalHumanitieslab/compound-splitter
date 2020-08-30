import os
import requests
from subprocess import Popen
from time import sleep

# default communication settings of the server
HOST = "localhost"
PORT = 51337

OWN_DIR = os.path.dirname(__file__)
BIN_DIR = os.path.join(OWN_DIR, "bin")
SERVER_PATH = os.path.join(OWN_DIR, "bin", "SECOS-master")

# server subprocess
server_proc = None


def split(word: str):
    response = requests.get(f'http://{HOST}:{PORT}?sentence={word}')
    splitted = response.text.lstrip()
    if not splitted:
        splitted = word
    return {
        "candidates": [
            {
                "parts": splitted.split(" "),
                "score": 1
            }
        ]
    }


def start():
    global server_proc
    server_proc = Popen(
        ["python",
         os.path.join(SERVER_PATH, "decompound_server.py"),
         # dt_candidates:   file with words and their split candidates, generated from a distributional thesaurus (DT)
         "data/dutchCoW_trigram__candidates",
         # word_count_file: file with word counts used for filtering
         "data/dutchCoW_trigram__WordCount",
         # min_word_count:  minimal word count used for split candidates (recommended paramater: 50)
         "50",
         # prefix_length:   length of prefixes that are appended to the right-sided word (recommended parameter: 3)
         "3",
         # suffix_length:   length of suffixes that are appended to the left-sided word (recommended parameter: 3)
         "3",
         # word_length:     minimal word length that is used from the split candidates (recommended parameter: 5)
         "5",
         # dash_word:       heuristic to split words with dash, which has no big impact (recommended: 3)
         "3",
         # upper:           consider uppercase letters (=upper) or not (=lower). Should be set for case-sensitive languages e.g. German
         "lower",
         # epsilon:         smoothing factor (recommended parameter: 0.01)
         "0.01",
         str(PORT)],
        cwd=SERVER_PATH)

    # wait for the server to start
    sleep(60)
    pass


def stop():
    global server_proc
    if server_proc:
        server_proc.terminate()
        server_proc.communicate()


def prepare():
    if not os.path.exists(os.path.join(BIN_DIR)):
        from zipfile import ZipFile
        # should have been retrieved using ~/retrieve.py
        with ZipFile(os.path.join(OWN_DIR, "..", "..", "dependencies", "secos.zip")) as archive:
            archive.extractall(BIN_DIR)

    if not os.path.exists(os.path.join(SERVER_PATH, "data")):
        from zipfile import ZipFile
        with ZipFile(os.path.join(OWN_DIR, "..", "..", "dependencies", "secos-nl.zip")) as archive:
            archive.extractall(SERVER_PATH)


prepare()
