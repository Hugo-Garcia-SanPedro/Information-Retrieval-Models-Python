# Information Retrieval Models in Python
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![NLP](https://img.shields.io/badge/field-NLP-orange)

This repository contains a comprehensive implementation of an **Information Retrieval (IR)** system, transitioning from classical logic to modern vector-based ranking and efficient indexing.

## 🚀 Overview
This project explores the core pillars of **Data Science** and **Natural Language Processing (NLP)**. It demonstrates how to build a search engine from the ground up, covering document preprocessing, various retrieval models, and optimized data structures designed for high-speed performance.

---

## 🛠 Project Milestones & Modules

The development is divided into six logical modules based on industry-standard IR specifications:

1.  **Text Normalization (`normalization.py`):** A preprocessing pipeline that handles ISO-8859-1/UTF-8 encodings, removes stop-words, and cleans text by removing punctuation and accents (Diacritics).
2.  **Boolean Retrieval (`boolean-model.py`):** A retrieval engine supporting exact matches using `AND` and `OR` logic.
3.  **Probabilistic Model (`probabilistic.py`):** Implementation of relevance-based retrieval including a manual feedback loop to refine results.
4.  **Vector Space Model (VSM) (`vector-model.py`):** Uses **tf-IDF weighting** and **Cosine Similarity** to rank documents by mathematical relevance.
5.  **Query Expansion:** * **Rocchio Algorithm:** Refines queries by incorporating user-defined relevant and non-relevant documents.
    * **Co-occurrence Matrix:** Expands queries by calculating term correlations using matrix multiplication ($M \times N \times N \times M$).
6.  **Inverted Indexing (`indexing.py`):** The final stage implements an industry-standard Inverted Index, mapping terms to document IDs and weights for optimized retrieval speed.

---

## 📑 Mathematical Background

The system leverages several mathematical models to determine document relevance:

### 1. TF-IDF Weighting
To assign importance to a term within a document:
$$w_{i,j} = tf_{i,j} \times \log_{10}\left(\frac{N}{df_i}\right)$$

### 2. Cosine Similarity (VSM)
To calculate the similarity between a query vector ($q$) and a document vector ($d_j$):
$$sim(d_j, q) = \frac{\vec{d_j} \cdot \vec{q}}{|\vec{d_j}| |\vec{q}|} = \frac{\sum_{i=1}^{n} w_{i,j} w_{i,q}}{\sqrt{\sum_{i=1}^{n} w_{i,j}^2} \sqrt{\sum_{i=1}^{n} w_{i,q}^2}}$$

### 3. Rocchio Feedback
To optimize the query vector based on user feedback:
$$\vec{q}_m = \alpha \vec{q}_0 + \beta \frac{1}{|D_r|} \sum_{\vec{d}_j \in D_r} \vec{d}_j - \gamma \frac{1}{|D_{nr}|} \sum_{\vec{d}_j \in D_{nr}} \vec{d}_j$$

---

## 📂 Repository Organization

```text
.
├── data/               # Original .txt documents and stop-words list
├── processed/          # Normalized .rep files (term lists)
├── src/                # Python source code
│   ├── normalization.py
│   ├── boolean-model.py
│   ├── vector-model.py
│   ├── probabilistic.py
│   ├── indexing.py
│   └── main.py         # Main orchestrator
└── docs/               # Technical specifications and PDFs
## 🧪 Technical Stack
* **Language:** Python 3.10+
* **Key Libraries:** 
    * `Re`: Regular expressions for advanced text cleaning.
    * `OS/Sys`: For Linux-style file system management.
