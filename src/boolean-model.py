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

# Function that resolve the query
def resolve_query():
    print("\n--- Boolean Model Query Resolution ---")
    print("Formats allowed: 'term1 AND term2', 'term1 OR term2'")
    raw_query = input("Write your query: ").strip()
    
    if not raw_query:
        print("Empty query.")
        return

    # 1. Parse the query to find the operator and terms
    # We assume simple queries: "A AND B" or "A OR B"
    parts = raw_query.split()
    
    operator = None
    terms = []

    # Detect operator (case insensitive)
    if "AND" in [p.upper() for p in parts]:
        operator = "AND"
        # Split by the word AND/and
        temp_terms = re.split(r'\s+AND\s+|\s+and\s+', raw_query)

    elif "OR" in [p.upper() for p in parts]:
        operator = "OR"
        temp_terms = re.split(r'\s+OR\s+|\s+or\s+', raw_query)

    else:
        print("No operator in the query.")
        return

    # 2. Normalize query terms to match .rep format
    # We filter out empty strings in case of extra spaces
    terms = [normalize_term(t) for t in temp_terms if t.strip()]
    
    if not terms:
        print("Invalid query terms.")
        return

    print(f"Searching for: {terms} with logic: {operator}")

    # 3. Iterate through all .rep files
    if not os.path.exists(PROCESSED_DIR):
        print(f"Error: {PROCESSED_DIR} does not exist.")
        return

    files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.rep')]
    matches = []

    for filename in files:
        filepath = os.path.join(PROCESSED_DIR, filename)
        content = read_file(filepath)
        
        # Create a SET of words from the document for O(1) lookup speed
        # The .rep file has terms separated by newlines or spaces
        doc_terms = set(content.split())
        
        is_match = False
        
        # 4. Check logic
        if operator == "AND":
            # ALL terms must be in the document
            # We use Python's set capability: is the set of query terms a subset of doc terms?
            if set(terms).issubset(doc_terms):
                is_match = True
                
        elif operator == "OR":
            # AT LEAST ONE term must be in the document
            # Intersection of sets must not be empty
            if not doc_terms.isdisjoint(set(terms)):
                is_match = True

        if is_match:
            # We store the original .txt name usually, or the .rep name
            matches.append(filename)

    # 5. Output results
    if matches:
        print(f"\nQuery found in {len(matches)} documents:")
        for m in matches:
            print(f" -> {m}")
    else:
        print("\nNo documents matched your query.")

# Function for main
def main():
    while True:
        print("\n=== BOOLEAN MODEL MENU ===")
        print("a) Query resolve")
        print("b) Exit")

        choice = input("Select an option: ").lower().strip()

        if choice == 'a':
            resolve_query()
        
        elif choice == 'b':
            print("Exiting...")
            break

        else:
            print("Invalid option. Please try again.")

# Main
if __name__ == "__main__":
    if not os.path.exists(PROCESSED_DIR):
        print(f"Error: Processed directory not found at {PROCESSED_DIR}")
        print("Please create the 'Processed' folder and add your .rep files.")
    
    else:
        main()