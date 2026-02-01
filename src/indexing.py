import os
import math
import sys
from collections import defaultdict, Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed')

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(list)
        
        # Mapping de IDs
        self.doc_map = {}
        
        self.vocab_list = []
        
        # State of the system
        self.is_built = False

    def load_content(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='iso-8859-1') as f:
                return f.read()

    def build_index(self):
        if not os.path.exists(PROCESSED_DIR):
            print(f"Error: The directory does not exits: {PROCESSED_DIR}")
            return

        # 1. Get .rep files
        files = sorted([f for f in os.listdir(PROCESSED_DIR) if f.endswith('.rep')])
        if not files:
            print("No .rep files in the directory 'processed'.")
            return

        print(f"Proccesing {len(files)} documents...")
        
        self.index = defaultdict(list)
        self.doc_map = {}

        doc_freqs = defaultdict(int) # DF
        doc_term_counts = {} # TF
        all_terms = set()
        N = len(files) # Total of documents

        # 2. TFs y DFs
        for idx, filename in enumerate(files):
            doc_id = idx + 1 
            self.doc_map[doc_id] = filename
            
            filepath = os.path.join(PROCESSED_DIR, filename)
            content = self.load_content(filepath)
            
            tokens = content.split()
            
            counts = Counter(tokens)
            doc_term_counts[doc_id] = counts
            
            for term in counts:
                doc_freqs[term] += 1
                all_terms.add(term)

        self.vocab_list = sorted(list(all_terms))

        # 3. (TF * IDF) 
        for term in self.vocab_list:
            df = doc_freqs[term]
            idf = math.log10(N / df) if df > 0 else 0
            
            # Search in which documents this term appears
            # (We iterate over the docs that we know contain the term to be efficient)
            # However, given the design, we iterate over the docs stored in memory:
            for doc_id in self.doc_map:
                tf = doc_term_counts[doc_id].get(term, 0)
                
                if tf > 0:
                    weight = tf * idf
                    self.index[term].append((doc_id, weight))

        self.is_built = True
        print("Index built successfully.")

    def show_full_index(self):
        if not self.is_built:
            print("Error: The index is not built. Run option (a) first.")
            return

        print("\n--- COMPLETE INVERTED INDEX ---")
        print(f"{'ID':<5} {'Term':<20} {'Postings [DocID: Weights]'}")
        print("-" * 60)
        
        for idx, term in enumerate(self.vocab_list):
            postings = self.index[term]
            postings_str = ", ".join([f"[{d}: {w:.4f}]" for d, w in postings])
            print(f"{idx+1:<5} {term:<20} {postings_str}")

    def show_term_info(self):
        if not self.is_built:
            print("Error: The index is not built. Run option (a) first.")
            return

        query = input("\nEnter a term or its number (ID): ").strip()
        
        target_term = ""

        if query.isdigit():
            term_idx = int(query) - 1
            if 0 <= term_idx < len(self.vocab_list):
                target_term = self.vocab_list[term_idx]
            else:
                print("Error: Term number out of range.")
                return
        else:
            target_term = query.lower()

        if target_term in self.index:
            postings = self.index[target_term]
            print(f"\n--- Information of term: '{target_term}' ---")
            print(f"Appears in {len(postings)} documents.")
            print("Details (DocID, Name, Weight):")
            for doc_id, weight in postings:
                doc_name = self.doc_map[doc_id]
                print(f"  -> Doc {doc_id} ({doc_name}): \tWeight {weight:.6f}")
        else:
            print(f"The term in the '{query}' does not exits in the vocabulary.")

def print_menu():
    print("n=== INVERTED INDEX MENU ===")
    print("a) Build index")
    print("b) Display the complete index on the screen")
    print("c) Information about a term")
    print("d) Exit")

def main():
    system = InvertedIndex()
    
    while True:
        print_menu()
        choice = input("Choose an option: ").strip().lower()

        if choice == 'a':
            system.build_index()
        
        elif choice == 'b':
            system.show_full_index()
            
        elif choice == 'c':
            system.show_term_info()
            
        elif choice == 'd':
            print("Exiting...")
            break
        
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()