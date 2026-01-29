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
    processed_files = list_files(PROCESSED_DIR, '.rep')
    if not processed_files:
        print("Error: No processed files (.rep) found in 'processed' directory.")
        return

    docs_index = {}
    total_docs_N = len(processed_files)

    for fname in processed_files:
        path = os.path.join(PROCESSED_DIR, fname)
        content = read_file(path)
        terms = set(content.split()) 
        docs_index[fname] = terms

    # The user insert the query
    raw_query = input("\nInsert the query: ").strip()
    query_terms = [normalize_term(t) for t in raw_query.split()]
    query_terms = [t for t in query_terms if t]

    if not query_terms:
        print("Empty query.")
        return

    # Inicialization of relevant variables
    relevant_docs_marked = set() 
    
    # Feedback Loop
    iteration = 0
    while True:
        iteration += 1
        print(f"\n=== RESULTS (Iteration {iteration}) ===")
        
        # Variables for the probabilistic formula (Robertson/Sparck Jones)
        # N: Total documents (total_docs_N)
        # R: Total known relevant documents
        R = len(relevant_docs_marked)
        
        scores = []

        for doc_name, doc_terms in docs_index.items():
            rsv = 0.0 
            
            for term in query_terms:
                if term in doc_terms: 
                    n_t = sum(1 for d in docs_index.values() if term in d)
                    r_t = sum(1 for d_name in relevant_docs_marked if term in docs_index[d_name])

                    # w = log( (r_t + 0.5) / (R - r_t + 0.5) / ((n_t - r_t + 0.5) / (N - n_t - R + r_t + 0.5)) )
                    numerator = (r_t + 0.5) / (R - r_t + 0.5)
                    denominator = (n_t - r_t + 0.5) / (total_docs_N - n_t - R + r_t + 0.5)
                    
                    weight = math.log(numerator / denominator)
                    rsv += weight
            
            scores.append((doc_name, rsv))

        # Show results
        scores.sort(key=lambda x: x[1], reverse=True)

        for idx, (doc, score) in enumerate(scores):
            marker = "[REL]" if doc in relevant_docs_marked else ""
            print(f"{idx + 1}. {doc} \t(Score: {score:.4f}) {marker}")

        print("\n--- Feedback Options ---")
        print("Enter the numbers of the RELEVANT documents separated by spaces.")
        print("Or press ENTER without typing anything to END the search.")
        
        selection = input("Selection: ").strip()
        
        if not selection:
            break
            
        try:
            indices = list(map(int, selection.split()))
            new_relevance_found = False
            
            for i in indices:
                if 1 <= i <= len(scores):
                    doc_name = scores[i-1][0]
                    if doc_name not in relevant_docs_marked:
                        relevant_docs_marked.add(doc_name)
                        new_relevance_found = True
                        print(f" -> Marked as relevant: {doc_name}")
                else:
                    print(f"Ignoring index out of range: {i}")
            
            if not new_relevance_found:
                print("No new relevant documents were added. Finishing...")
                break
                
        except ValueError:
            print("Invalid entry. Please enter numbers only.")

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