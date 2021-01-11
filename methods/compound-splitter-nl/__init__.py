import os
import socket
from subprocess import Popen
from time import sleep

# default communication settings of the server
HOST = "localhost"
PORT = 50500

OWN_DIR = os.path.dirname(__file__)
BIN_DIR = os.path.join(OWN_DIR, "bin")

# server subprocess
server_proc = None


def split(word: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection:
        connection.connect((HOST, PORT))
        connection.sendall((word + "\n").encode())

        # rstrip to remove the newline
        splitted = connection.recv(1024).decode().rstrip()
        if not splitted:
            # no split applied
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
    server_path = os.path.join(BIN_DIR, "compound-splitter-nl")
    server_proc = Popen(
        ["perl", os.path.join(server_path, "compound_server.pl")],
        cwd=server_path,
        env={"PERL5LIB": server_path})

    # wait for the server to start
    sleep(10)


def stop():
    global server_proc
    if server_proc:
        server_proc.terminate()
        server_proc.communicate()


def prepare():
    if not os.path.exists(os.path.join(BIN_DIR)):
        import tarfile
        # should have been retrieved using ~/retrieve.py
        tar = tarfile.open(os.path.join(OWN_DIR, "..", "..",
                                        "dependencies", "compound-splitter-nl.tar.gz"))
        tar.extractall(BIN_DIR)
