import os
import re
import unicodedata
import sys

# --- Configuration Paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed')
STOPWORDS_FILE = os.path.join(DATA_DIR, 'stopwords.txt') 

def load_stopwords(filepath):
    if not os.path.exists(filepath):
        print(f"Warning: Stopwords file not found at {filepath}")
        return set()
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return set(word.strip().lower() for word in f)
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='iso-8859-1') as f:
            return set(word.strip().lower() for word in f)

def remove_accents(text):
    """Normalizes text to remove tildes (e.g., 'canción' -> 'cancion')."""
    # NFD decomposes characters 
    nfkd_form = unicodedata.normalize('NFD', text)
    # We filter out non-spacing mark characters
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def clean_text(text, stopwords):
    """
    1. Lowercase
    2. Remove accents
    3. Remove punctuation 
    4. Remove stop words
    """
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove accents
    text = remove_accents(text)
    
    # 3. Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text)
    
    # 4. Tokenize (split by whitespace)
    tokens = text.split()
    
    # 5. Remove Stopwords
    clean_tokens = [t for t in tokens if t not in stopwords]
    
    return clean_tokens

def read_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding='iso-8859-1') as f:
            return f.read()

def save_rep_file(filename, tokens):
    """Saves the normalized tokens into a .rep file."""
    if not os.path.exists(PROCESSED_DIR):
        os.makedirs(PROCESSED_DIR)
        
    rep_filename = os.path.splitext(filename)[0] + ".rep"
    rep_path = os.path.join(PROCESSED_DIR, rep_filename)
    
    with open(rep_path, 'w', encoding='utf-8') as f:
        # Saving tokens separated by newlines
        f.write("\n".join(tokens))
    
    return rep_filename

def list_files(directory, extension):
    if not os.path.exists(directory):
        return []
    return sorted([f for f in os.listdir(directory) if f.endswith(extension)])

# --- Menu Functions ---
def menu_list_originals():
    files = list_files(DATA_DIR, '.txt')
    print("\n--- Original Documents ---")
    for f in files:
        print(f" - {f}")

def menu_list_normalized():
    files = list_files(PROCESSED_DIR, '.rep')
    print("\n--- Normalized Documents (.rep) ---")
    for f in files:
        print(f" - {f}")

def menu_show_original():
    fname = input("Enter filename (e.g., file01.txt): ").strip()
    path = os.path.join(DATA_DIR, fname)
    if os.path.exists(path):
        content = read_file(path)
        print(f"\n--- Content of {fname} ---")
        print(content)
        print("-----------------------------")
    else:
        print("Error: File not found.")

def menu_show_normalized():
    fname = input("Enter filename (e.g., file01.rep): ").strip()
    
    if fname.endswith('.txt'):
        fname = fname.replace('.txt', '.rep')
        
    path = os.path.join(PROCESSED_DIR, fname)
    if os.path.exists(path):
        content = read_file(path)
        print(f"\n--- Content of {fname} ---")
        print(content) # Lists terms
        print("-----------------------------")
    else:
        print("Error: File not found. Have you normalized it yet?")

def menu_normalize_doc(stopwords):
    fname = input("Enter filename to normalize (or 'all' for all files): ").strip()
    
    files_to_process = []
    if fname.lower() == 'all':
        files_to_process = list_files(DATA_DIR, '.txt')
    else:
        path = os.path.join(DATA_DIR, fname)
        if os.path.exists(path):
            files_to_process = [fname]
        else:
            print("Error: File not found.")
            return

    for f in files_to_process:
        full_path = os.path.join(DATA_DIR, f)
        raw_text = read_file(full_path)
        tokens = clean_text(raw_text, stopwords)
        out_name = save_rep_file(f, tokens)
        print(f"Processed: {f} -> {out_name} ({len(tokens)} terms)")

def main():
    stopwords = load_stopwords(STOPWORDS_FILE)
    print(f"Loaded {len(stopwords)} stopwords.")

    while True:
        print("\n=== TEXT NORMALIZATION MENU ===")
        print("a) List original documents")
        print("b) List normalized documents")
        print("c) Show original document content")
        print("d) Show normalized document content")
        print("e) Normalize a document")
        print("f) Exit")
        
        choice = input("Select an option: ").lower().strip()

        if choice == 'a':
            menu_list_originals()
        elif choice == 'b':
            menu_list_normalized()
        elif choice == 'c':
            menu_show_original()
        elif choice == 'd':
            menu_show_normalized()
        elif choice == 'e':
            menu_normalize_doc(stopwords)
        elif choice == 'f':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        print(f"Error: Data directory not found at {DATA_DIR}")
        print("Please create the 'data' folder and add your .txt files.")
    else:
        main()