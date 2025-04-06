# searchEngine.py
import pickle
import re
import time
import os
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

INDEX_PATH = "../data/index.pkl"
DOCS_PATH = "../data/docs.pkl"

inverted_index = {}
documents = {}

# Load index
if os.path.exists(INDEX_PATH) and os.path.exists(DOCS_PATH):
    with open(INDEX_PATH, "rb") as f:
        inverted_index = pickle.load(f)
    with open(DOCS_PATH, "rb") as f:
        documents = pickle.load(f)
else:
    print("Index not found. Please run the indexing script first.")

stemmer = PorterStemmer()

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    return [stemmer.stem(word) for word in tokens]

# Search
# Boolean Search - Can use Logic Operators in queries (AND, OR, NOT) sort by frequency, and return a context snippet
def boolean_search(query, window_size=50):
    start_time = time.time()  # Start timing for performance measure, so we can see how long it takes to search

    words = preprocess(query)  # Preprocess query to get stemmed tokens
    if not words:
        return {"results": [], "search_time": 0, "total_time": 0}

    search_start = time.time()

    # Handling Boolean operators (AND, OR, NOT)
    and_sets = []
    or_set = set()
    not_set = set()

    operator = "OR"  # Default operator is OR
    for word in words:
        if word.upper() == "AND":
            operator = "AND"
        elif word.upper() == "OR":
            operator = "OR"
        elif word.upper() == "NOT":
            operator = "NOT"
        else:
            if operator == "AND":
                and_sets.append(set(inverted_index.get(word, {}).keys()))
            elif operator == "OR":
                or_set.update(inverted_index.get(word, {}).keys())
            elif operator == "NOT":
                not_set.update(inverted_index.get(word, {}).keys())

    # Apply AND logic
    if and_sets:
        result_set = set.intersection(*and_sets) if and_sets else set()
    else:
        result_set = or_set  # If no AND, use OR set

    # Apply NOT logic
    result_set -= not_set

    # Rank results by frequency
    doc_scores = {}
    for word in words:
        for doc, freq in inverted_index.get(word, {}).items():
            if doc in result_set:
                doc_scores[doc] = doc_scores.get(doc, 0) + freq

    # Sort results by frequency (highest first)
    sorted_results = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

    # Extract context snippets for each document
    final_results = []
    for doc, score in sorted_results:
        text = documents.get(doc, "")  # Get full text of the document
        snippets = []

        for word in words:
            word_positions = [m.start() for m in re.finditer(r'\b' + re.escape(word) + r'\b', text)]
            for pos in word_positions:
                start = max(0, pos - window_size)
                end = min(len(text), pos + window_size)
                snippet = f"...{text[start:end]}..."
                snippets.append(snippet)

        final_results.append({
            "document": doc,
            "score": score,
            "snippets": snippets
        })

    search_time = time.time() - search_start
    total_time = time.time() - start_time

    return {
        "results": final_results,
        "search_time": round(search_time, 4),
        "total_time": round(total_time, 4)
    }

'''Example Return data:

{
    "results": [
        {
            "document": "Einstein_Relativity.pdf",
            "score": 15,  # Total frequency of all matched words
            "snippets": [
                "...the principles of quantum mechanics were found to complement Einstein's theory...",
                "...relativity suggests that time is not absolute but depends on the observer..."
            ]
        },
        {
            "document": "Quantum_Theory.pdf",
            "score": 12,
            "snippets": [
                "...in quantum mechanics, we describe particles as probabilistic wave functions..."
            ]
        }
    ],
    "search_time": 0.0034,
    "total_time": 0.0071
}

'''