import os
import re
import unicodedata
import math
import sys

# Configuration Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed')
STOPWORDS_FILE = os.path.join(DATA_DIR, 'stopwords.txt')

# Function dor read the files
def read_file(filepath):
    try:
        with open(filepath, 'r', encoding = 'utf-8') as f:
            return f.read()
        
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding = 'iso-8859-1') as f:
            return f.read()

# Function for normalize the terms
def remove_accents(text):
    nfkd_form = unicodedata.normalize('NFD', text)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def normalize_term(term):
    term = term.lower().strip()
    term = remove_accents(term)
    term = re.sub(r'[^\w\s]', '', term)
    return term