import os
import pymupdf
import pickle
import math
from collections import defaultdict
import preprocess
import config


def extract_text_from_pdf(path):
    try:
        doc = pymupdf.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return ""


def document_index(folder=config.DOCS_PATH):
    inverted_index = defaultdict(lambda: defaultdict(int))
    documents = {}
    docPreprocessed = {}
    df = defaultdict(int)
    doc_lengths = {}
    doc_terms = {} #filename → list of original (non-preprocessed) words

    for filename in os.listdir(folder):
        if not filename.endswith(".pdf"):
            continue

        path = os.path.join(folder, filename)
        print(f"Indexing: {filename}")
        text = extract_text_from_pdf(path)
        if not text:
            continue

        documents[filename] = text
        original_terms = text.split()
        tokens = preprocess.preprocess(text)
        doc_terms[filename] = original_terms  # Just store original terms (you can refine)
        docPreprocessed[filename] = tokens

        term_counts = defaultdict(int)
        for token in tokens:
            term_counts[token] += 1

        for term, tf in term_counts.items():
            inverted_index[term][filename] = tf

    for term, postings in inverted_index.items():
        df[term] = len(postings)

    N = len(documents)
    for filename in documents:
        length = 0
        for term in inverted_index:
            if filename in inverted_index[term]:
                tf = inverted_index[term][filename]
                idf = math.log((N + 1) / (df[term] + 1))
                tf_idf = tf * idf
                length += tf_idf ** 2
        doc_lengths[filename] = math.sqrt(length)

    with open(config.INDEX_PICKLE, "wb") as f:
        pickle.dump(dict(inverted_index), f)
    with open(config.DOCS_PICKLE, "wb") as f:
        pickle.dump(documents, f)
    with open(config.DF_PICKLE, "wb") as f:
        pickle.dump(dict(df), f)
    with open(config.DOC_LENGTHS_PICKLE, "wb") as f:
        pickle.dump(doc_lengths, f)
    with open(config.TERMS_PICKLE, "wb") as f:
        pickle.dump(doc_terms, f)
    with open(config.PREPROCESSED_TERMS_PICKLE, "wb") as f:
        pickle.dump(docPreprocessed, f)

    print("Indexing complete.")


if __name__ == "__main__":
    document_index()
