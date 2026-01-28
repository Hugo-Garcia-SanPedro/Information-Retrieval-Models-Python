# Information Retrieval Models in Python

This repository contains a comprehensive implementation of an Information Retrieval (IR) system, transitioning from classical logic to modern vector-based ranking and efficient indexing.

## 🚀 Overview
This project explores the core pillars of **Data Science** and **Natural Language Processing (NLP)**. This Python implementation demonstrates how to build a search engine from the ground up, covering document preprocessing, various retrieval models, and optimized data structures.

## 🛠 Project Structure & Milestones

The development is divided into six logical modules based on the project specifications:

1. **Text Normalization:** A preprocessing pipeline that handles ISO-8859-1/UTF-8 encodings, removes stop-words, and cleans text by removing punctuation and accents.
2. **Boolean Retrieval:** A retrieval engine supporting `AND` and `OR` logic to find exact matches across the document collection.
3. **Probabilistic Model:** An implementation of relevance-based retrieval including a manual feedback loop.
4. **Vector Space Model (VSM):** Uses **tf-IDF weighting** and **Cosine Similarity** to rank documents by mathematical relevance.
5. **Query Expansion:** * **Rocchio Algorithm:** Refines queries by incorporating user-defined relevant and non-relevant documents.
    * **Co-occurrence Matrix:** Expands queries by calculating term correlations using matrix multiplication ($M \times N \times N \times M$).
6. **Inverted Indexing:** The final stage implements an industry-standard Inverted Index, mapping terms to document IDs and weights for high-speed retrieval.

## 📂 Repository Organization
* `/src`: Python source code for each retrieval model.
* `/data`: Original `.txt` documents and the "stop-words" list.
* `/processed`: Normalized `.rep` files representing documents as term lists.
* `/docs`: Original PDF specifications for each practice.

## 🧪 Technical Stack
* **Language:** Python 3.10+
* **Key Libraries:** `NumPy`: For high-performance matrix operations ($tf-IDF$ and Co-occurrence).
    * `Re`: Regular expressions for advanced text cleaning.
    * `OS/Sys`: For Linux-style file system management.
