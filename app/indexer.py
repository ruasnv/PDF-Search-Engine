# indexer.py
import os
import re
import pymupdf
import pickle
from collections import defaultdict
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

INDEX_PATH = "./data/index.pkl"
DOCS_PATH = "D:/books"

stemmer = PorterStemmer()

def extract_text_from_pdf(path):
    try:
        doc = mymupdf.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return ""

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = word_tokenize(text)
    return [stemmer.stem(word) for word in tokens]

def index_documents(folder=DOCS_PATH):
    inverted_index = defaultdict(lambda: defaultdict(int))
    documents = {}

    for filename in os.listdir(folder):
        if filename.endswith(".pdf"):
            path = os.path.join(folder, filename)
            print(f"Indexing: {filename}")
            text = extract_text_from_pdf(path)
            if text:
                documents[filename] = text
                tokens = preprocess(text)
                for word in tokens:
                    inverted_index[word][filename] += 1
        else:
            print(f"Skipping {filename} (not a PDF)")

    # Convert defaultdict to regular dicts before pickling. Pickle uses core objects only.
    inverted_index = {k: dict(v) for k, v in inverted_index.items()}

    with open(INDEX_PATH, "wb") as f:
        pickle.dump((inverted_index, documents), f)

    print(f"Indexing complete. {len(documents)} documents indexed.")
    print(f"Index saved at: {INDEX_PATH}")

if __name__ == "__main__":
    index_documents()
