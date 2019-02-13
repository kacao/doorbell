import os
import vlc

def abspath(p):
    return os.path.abspath(p)

def sanitize(s):
    s = s[:20]
    s = s.replace('/', '')
    s = s.replace('\\', '')
    s = s.replace('\'', '')
    s = s.replace('\"', '')
    return s 

def join(path, filename):
    return os.path.join(path, filename)

def exists(filepath):
    return os.path.isfile(filepath)
