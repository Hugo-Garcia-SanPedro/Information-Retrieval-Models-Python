import os
import re
import unicodedata
import math
import sys
from collections import defaultdict, Counter

# Configuration Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed')
STOPWORDS_FILE = os.path.join(DATA_DIR, 'stopwords.txt')

# Rocchio Hyperparameters
ALPHA = 1.0 # Original query weight
BETA = 0.75 # Relevant documents weight
GAMMA = 0.15 # Non-relevant documents weight

# Function dor read the files
def read_file(filepath):
    try:
        with open(filepath, 'r', encoding = 'utf-8') as f:
            return f.read()
        
    except UnicodeDecodeError:
        with open(filepath, 'r', encoding = 'iso-8859-1') as f:
            return f.read()
        
    except FileNotFoundError:
        return None

# Function for normalize the terms
def remove_accents(text):
    nfkd_form = unicodedata.normalize('NFD', text)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

def normalize_term(term):
    term = term.lower().strip()
    term = remove_accents(term)
    term = re.sub(r'[^\w\s]', '', term)
    return term

def load_stopwords():
    stops = set()
    if os.path.exists(STOPWORDS_FILE):
        content = read_file(STOPWORDS_FILE)
        if content:
            # Assumes stopwords are separated by newlines or spaces
            for word in content.split():
                stops.add(normalize_term(word))
    
    return stops

def tokenize(text, stopwords):
    words = text.split()
    tokens = []
    for w in words:
        norm = normalize_term(w)
        if norm and norm not in stopwords and not norm.isnumeric():
            tokens.append(norm)

    return tokens

# Vector Space Model Logic

# Function for main and menu
def print_menu():
    print("\n--- VECTOR MODEL (ROCCHIO) ---")
    print("a) List the documents.")
    print("b) Show a document.")
    print("c) Show the vector of a document.")
    print("d) Show the vocabulary.")
    print("e) Show frequency table.")
    print("f) Resolve a query with feedback.")
    print("g) Exit.")

def main():
    engine = SearchEngine()
    engine.load_documents()

    if len(engine.documents) == 0:
        print("No documents have been uploaded. Check the 'data' directory.")
        # We allow the program to continue but most options will be empty
        
    while True:
        print_menu()
        choice = input("Choose an option: ").lower().strip()

        if choice == 'a':
            print("\nAvailable documents:")
            for doc in engine.documents.keys():
                print(f" - {doc}")

        elif choice == 'b':
            fname = input("Insert the name of the file (ej: d1.txt): ")
            if fname in engine.documents:
                print(f"\n--- Content of {fname} ---")
                print(engine.documents[fname])
            else:
                print("Error: Document not found.")

        elif choice == 'c':
            fname = input("Insert the name of the file (ej: d1.txt): ")
            if fname in engine.weights:
                print(f"\n--- (Weights TF-IDF) of {fname} ---")
                # Showing only non-zero weights for readability
                vec = {k: v for k, v in engine.weights[fname].items() if v > 0}
                print(vec)
            else:
                print("Error: Document no found.")

        elif choice == 'd':
            print(f"\n--- Vocabulary ({len(engine.vocab)} terms) ---")
            print(", ".join(engine.vocab))

        elif choice == 'e':
            print("\n--- Frecuency Table ---")
            # Header
            docs = list(engine.documents.keys())
            header = "{:<15}".format("Term") + "".join([f"{d[:8]:<10}" for d in docs])
            print(header)
            print("-" * len(header))
            
            for term in engine.vocab:
                row = "{:<15}".format(term)
                for doc in docs:
                    freq = engine.tf[doc].get(term, 0)
                    row += f"{freq:<10}"
                print(row)

        elif choice == 'f':
            query_str = input("\nIntroduce the query: ")
            q_vec = engine.get_query_vector(query_str)
            
            # Initial Search
            results = engine.search(q_vec)
            
            print(f"\nPreliminary results ({len(results)}):")
            for i, (doc, score) in enumerate(results):
                print(f"[{i+1}] {doc} (Sim: {score:.4f})")
            
            if not results:
                print("No matches found.")
                continue

            # Feedback Interaction
            print("\n--- (Rocchio) ---")
            print("Indicate the indices (numbers on the left) of the documents...")
            
            try:
                rel_input = input("Relevant (separate with space, press enter if none): ")
                nrel_input = input("Not Relevant (separate with space, press enter if none): ")
                
                rel_indices = [int(x)-1 for x in rel_input.split()] if rel_input else []
                nrel_indices = [int(x)-1 for x in nrel_input.split()] if nrel_input else []
                
                # Map indices to filenames
                rel_docs = [results[i][0] for i in rel_indices if 0 <= i < len(results)]
                nrel_docs = [results[i][0] for i in nrel_indices if 0 <= i < len(results)]
                
                print(f"\nRelevant: {rel_docs}")
                print(f"Not Relevant: {nrel_docs}")

                # Calculate new query
                new_q_vec = engine.rocchio_feedback(q_vec, rel_docs, nrel_docs)
                
                # Search with new query
                new_results = engine.search(new_q_vec)
                
                print(f"\n--- Final Results (Post-Rocchio) ---")
                for i, (doc, score) in enumerate(new_results):
                    print(f"[{i+1}] {doc} (Sim: {score:.4f})")
                    
            except ValueError:
                print("Index entry error.")

        elif choice == 'g':
            print("Exiting...")
            break
        else:
            print("Invalid option.")

if __name__ == '__main__':
    main()