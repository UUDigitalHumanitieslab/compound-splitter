import os
from shutil import copyfile
import subprocess

OWN_DIR = os.path.dirname(__file__)
BIN_DIR = os.path.join(OWN_DIR, "bin")

def split(word: str):
    #run java script as subprocess
    p = subprocess.Popen(["java", "-jar", "MCS.jar", "--SPLIT", 
                          "--TERM", word, 
                          "--LEMMASET", "MCS_lemmaset.tsv", 
                          "--headMOPs", "MCS_mopset.tsv", 
                          "--modifierMOPs", "MCS_mopset.tsv", 
                          ], 
        cwd = BIN_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = p.communicate()
    total_output = out.decode().strip()

    #parse and format output
    def result(candidate_rank, candidate_output):
        fields = candidate_output.split("\t")
        parts = fields[6].lower().split()
        score = 1 / (candidate_rank + 1)
        return {"parts": parts, "score": score}

    candidates = [result(rank, output) for rank, output in enumerate(total_output.splitlines())]
    return { "candidates": candidates }

def start():
    pass

def stop():
    pass

def prepare():
    if not os.path.exists(BIN_DIR):
        # should have been retrieved using ~/retrieve.py
        os.mkdir(BIN_DIR)
        
        def copy_resource(filename):
            copyfile(os.path.join(OWN_DIR, "..", "..", "dependencies", filename), os.path.join(BIN_DIR, filename) )
        copy_resource("MCS.jar")
        copy_resource("MCS_lemmaset.tsv")
        copy_resource("MCS_mopset.tsv")

prepare()