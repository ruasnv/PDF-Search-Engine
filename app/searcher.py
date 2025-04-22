import pickle
import math
import time
import re
import os
from preprocess import preprocess
import config

inverted_index = {}
documents = {}

# Load index
if os.path.exists(config.INDEX_PATH) and os.path.exists(config.DOC_INDEX):
    with open(config.INDEX_PATH, "rb") as f:
        inverted_index = pickle.load(f)
    with open(config.DOC_INDEX, "rb") as f:
        documents = pickle.load(f)
else:
    print("Index not found. Please run the indexing script first.")


# Search
def search(query, window_size=20):
    start_time = time.time()
    words = preprocess(query)
    if not words:
        return {"results": [], "search_time": 0, "total_time": 0}

    search_start = time.time()

    # Collect all matching documents (OR logic)
    candidate_docs = set()
    for word in words:
        candidate_docs.update(inverted_index.get(word, {}).keys())

    # Compute IDF for each query term
    N = len(documents)
    idf = {}
    for word in words:
        df = len(inverted_index.get(word, {}))
        idf[word] = math.log((N + 1) / (df + 1)) + 1  # Smoothed IDF

    # Score documents using TF-IDF
    doc_scores = {}
    for word in words:
        postings = inverted_index.get(word, {})
        for doc, tf in postings.items():
            if doc not in candidate_docs:
                continue
            tfidf = (1 + math.log(tf)) * idf[word]
            doc_scores[doc] = doc_scores.get(doc, 0) + tfidf

    # Sort results by TF-IDF score
    sorted_results = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

    # KWIQ snippet generation
    final_results = []
    for doc, score in sorted_results:
        text = documents.get(doc, "")
        lower_text = text.lower()
        snippets = []

        for word in words:
            stemmed_word = word.lower()
            for match in re.finditer(
                r"\b" + re.escape(stemmed_word) + r"\b", lower_text
            ):
                start = max(0, match.start() - window_size)
                end = min(len(text), match.end() + window_size)
                snippet = f"...{text[start:end].strip()}..."
                snippets.append(snippet)

        final_results.append(
            {"document": doc, "score": round(score, 4), "snippets": snippets}
        )

    search_time = time.time() - search_start
    total_time = time.time() - start_time

    return {
        "query": query,
        "results": final_results,
        "search_time": round(search_time, 4),
        "total_time": round(total_time, 4),
    }


"""def boolean_search(query, window_size=50):
    start_time = time.time()  # Start timing for performance measure, so we can see how long it takes to search

    words = preprocess.preprocess(query)  # Preprocess query to get stemmed tokens
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
        "query":query,
        "results": final_results,
        "search_time": round(search_time, 4),
        "total_time": round(total_time, 4)
    }"""
