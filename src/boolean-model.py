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

# Function for solve a query
def resolve_query():
    query = input("Write your query (Ej: Dog AND cat): ").lower().strip()
    print(query)

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