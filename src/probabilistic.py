import os
import re
import unicodedata
import sys

# Configuration Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed')
STOPWORDS_FILE = os.path.join(DATA_DIR, 'stopwords.txt')

# Function for read the files
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

# Function to list de documents
def list_files(directory, extension):
    if not os.path.exists(directory):
        return []
    return sorted([f for f in os.listdir(directory) if f.endswith(extension)])

# Function to show normalized documents
def menu_list_normalized():
    files = list_files(PROCESSED_DIR, '.rep')
    print("\n--- Normalized Documents (.rep) ---")

    for f in files:
        print(f" - {f}")

# Function to show a original document
def menu_show_original():
    fname = input("Enter filename (e.g, file01.txt):").strip()
    path = os.path.join(DATA_DIR, fname)

    if os.path.exists(path):
        content = read_file(path)
        print(f"\n--- Content of {fname} ---")
        print(content)
        print("------------------------------")
    
    else:
        print("Error: File not found.")

# Function to show a normalized document
def menu_show_normalized():
    fname = input("Enter filename (e.g., file01.rep): ").strip()
    
    if fname.endswith('.txt'):
        fname = fname.replace('.txt', '.rep')
        
    path = os.path.join(PROCESSED_DIR, fname)
    if os.path.exists(path):
        content = read_file(path)
        print(f"\n--- Content of {fname} ---")
        print(content) 
        print("-----------------------------")

    else:
        print("Error: File not found. Have you normalized it yet?")

# Function to resolve a query, with the probabilistic method
def resolve_query():
    print("Hola")

# Function for main
def main():
    while True:
        print("\n=== PROBABILISTIC MODEL MENU ===")
        print("a) List the documents.")
        print("b) Show a document (.txt).")
        print("c) Show a document (.rep).")
        print("d) Solve a query.")
        print("f) Exit")

        choice = input("Select an option: ").lower().strip()

        if choice == 'a':
            menu_list_normalized()

        elif choice == 'b':
            menu_show_original()

        elif choice == 'c':
            menu_show_normalized()

        elif choice == 'd':
            resolve_query()

        elif choice == 'f':
            print("Exiting...")
            break

        else:
            print("Invalid option. PLeade try again.")

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        print(f"Error: Data directory not found at {DATA_DIR}")
        print("Please create the 'data' folder and add your .txt files.")

    else:
        main()