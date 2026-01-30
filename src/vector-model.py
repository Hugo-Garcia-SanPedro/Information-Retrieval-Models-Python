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
class SearchEngine:
    def __init__(self):
        self.documents = {} # {filename: content}
        self.doc_tokens = {} # {filename: [tokens]}
        self.vocab = sorted([]) 
        self.tf = {} # {filename: {term: freq}}
        self.idf = {} # {term: idf_val}
        self.weights = {} # {filename: {term: tf-idf}}
        self.stopwords = load_stopwords()

    def load_documents(self):
        # Reads all rep files from PROCESSED_DIR.
        if not os.path.exists(PROCESSED_DIR):
            print(f"Error: Directory {PROCESSED_DIR} does not exist.")
            return

        files = [f for f in os.listdir(PROCESSED_DIR) if f.endswith('.rep')]
        if not files:
            print("No .rep files found in data directory.")
            return

        print(f"Loading {len(files)} documents...")
        all_terms = set()

        for filename in files:
            path = os.path.join(PROCESSED_DIR, filename)
            content = read_file(path)
            self.documents[filename] = content
            
            # Tokenize
            tokens = tokenize(content, self.stopwords)
            self.doc_tokens[filename] = tokens
            
            # Calculate TF (Raw Frequency)
            term_counts = Counter(tokens)
            self.tf[filename] = term_counts
            all_terms.update(term_counts.keys())

        self.vocab = sorted(list(all_terms))
        self.calculate_weights()

    def calculate_weights(self):
        """Calculates TF-IDF for all documents."""
        N = len(self.documents)
        
        # Calculate IDF
        for term in self.vocab:
            # df: number of docs containing the term
            df = sum(1 for f in self.documents if term in self.tf[f])
            self.idf[term] = math.log10(N / df) if df > 0 else 0

        # Calculate TF-IDF Weights
        for filename in self.documents:
            self.weights[filename] = {}
            for term in self.vocab:
                tf_val = self.tf[filename].get(term, 0)
                # Standard TF*IDF. 
                # Note: Some implementations use (1+log(tf)), but prompts usually imply raw tf * idf
                w = tf_val * self.idf[term]
                self.weights[filename][term] = w

    def get_query_vector(self, query_str):
        # Converts query string to a vector (dict) using system IDF.
        tokens = tokenize(query_str, self.stopwords)
        tf_q = Counter(tokens)
        query_vec = {}
        
        for term in self.vocab:
            # Query weight = tf(in query) * idf(from collection)
            tf_val = tf_q.get(term, 0)
            query_vec[term] = tf_val * self.idf.get(term, 0)
            
        return query_vec

    def cosine_similarity(self, vec_a, vec_b):
        # Calculates cosine similarity between two vectors (dicts).
        dot_product = 0.0
        norm_a = 0.0
        norm_b = 0.0

        # We iterate over the vocabulary to ensure alignment
        for term in self.vocab:
            val_a = vec_a.get(term, 0)
            val_b = vec_b.get(term, 0)
            
            dot_product += val_a * val_b
            norm_a += val_a ** 2
            norm_b += val_b ** 2

        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return dot_product / (math.sqrt(norm_a) * math.sqrt(norm_b))
    
    def search(self, query_vec):
        # Returns sorted list of (filename, score).
        scores = []
        for filename, doc_vec in self.weights.items():
            sim = self.cosine_similarity(query_vec, doc_vec)
            if sim > 0:
                scores.append((filename, sim))
        
        # Sort by score descending
        return sorted(scores, key=lambda x: x[1], reverse=True)
    
    def rocchio_feedback(self, original_q_vec, rel_docs, non_rel_docs):
        # Implements: q_m = alpha*q_0 + beta*(1/|Dr| * sum(Dr)) - gamma*(1/|Dnr| * sum(Dnr))
        new_q_vec = {}

        # Pre-calculate centroids
        # We need to process every term in the vocabulary
        for term in self.vocab:
            # 1. Alpha * Original
            val_original = original_q_vec.get(term, 0) * ALPHA
            
            # 2. Beta * Average Relevant
            sum_rel = sum(self.weights[doc][term] for doc in rel_docs)
            avg_rel = (sum_rel / len(rel_docs)) if rel_docs else 0
            val_rel = BETA * avg_rel
            
            # 3. Gamma * Average Non-Relevant
            sum_nrel = sum(self.weights[doc][term] for doc in non_rel_docs)
            avg_nrel = (sum_nrel / len(non_rel_docs)) if non_rel_docs else 0
            val_nrel = GAMMA * avg_nrel
            
            # Combine
            new_weight = val_original + val_rel - val_nrel
            
            # Negative weights are usually handled by setting to 0 in standard VSM,
            # though strict Rocchio allows them (to penalize terms). 
            # We will keep them, but cosine handles them naturally (penalizing match).
            if new_weight < 0: 
                new_weight = 0 # It is safer to clamp to 0 for standard search engines
                
            new_q_vec[term] = new_weight
            
        return new_q_vec

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
            fname = input("Insert the name of the file (ej: d1.rep): ")
            if fname in engine.documents:
                print(f"\n--- Content of {fname} ---")
                print(engine.documents[fname])
            else:
                print("Error: Document not found.")

        elif choice == 'c':
            fname = input("Insert the name of the file (ej: d1.rep): ")
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