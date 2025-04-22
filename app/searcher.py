import pickle
import math
import time
from preprocess import preprocess
import config

# Load all needed files
with open(config.INDEX_PICKLE, "rb") as f:
    inverted_index = pickle.load(f)
with open(config.DOCS_PICKLE, "rb") as f:
    documents = pickle.load(f)
with open(config.DF_PICKLE, "rb") as f:
    df = pickle.load(f)
with open(config.DOC_LENGTHS_PICKLE, "rb") as f:
    doc_lengths = pickle.load(f)
with open(config.TERMS_PICKLE, "rb") as f:
    doc_terms = pickle.load(f)
with open(config.PREPROCESSED_TERMS_PICKLE, "rb") as f:
    docPreprocessed = pickle.load(f)

# Search function
def search(query, window_size=10):
    start_time = time.time()
    words = preprocess(query)
    if not words:
        return {"results": [], "search_time": 0, "total_time": 0}

    search_start = time.time()
    candidate_docs = set()
    for word in words:
        candidate_docs.update(inverted_index.get(word, {}))

    N = len(documents)
    idf = {word: math.log((N + 1) / (len(inverted_index.get(word, {})) + 1)) + 1 for word in words}

    doc_scores = {}
    for word in words:
        postings = inverted_index.get(word, {})
        for doc, tf in postings.items():
            tfidf = (1 + math.log(tf)) * idf[word]
            doc_scores[doc] = doc_scores.get(doc, 0) + tfidf

    sorted_results = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

    final_results = []
    for doc, score in sorted_results:
        content = docPreprocessed.get(doc, [])  # preprocessed token list
        snippets = []
        seen = set()
        for term in words:
            if term in seen or term not in content:
                continue
            seen.add(term)
            match_idx = content.index(term)
            start = max(0, match_idx - window_size)
            end = min(len(content), match_idx + window_size + 1)
            snippet_tokens = content[start:match_idx] + [f"<strong>{content[match_idx]}</strong>"] + content[match_idx+1:end]
            snippet = ' '.join(snippet_tokens)
            snippets.append(snippet)

        final_results.append({
            "document": doc,
            "score": round(score, 4),
            "snippets": snippets
        })

    search_time = time.time() - search_start
    total_time = time.time() - start_time

    return {
        "query": query,
        "results": final_results,
        "search_time": round(search_time, 4),
        "total_time": round(total_time, 4)
    }