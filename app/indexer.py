import os
import pymupdf
import pickle
import preprocess
import config
from collections import defaultdict


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


def index_documents(folder=config.DOCS_PATH):
    inverted_index = defaultdict(lambda: defaultdict(int))
    documents = {}

    for filename in os.listdir(folder):
        if filename.endswith(".pdf"):
            path = os.path.join(folder, filename)
            print(f"Indexing: {filename}")
            text = extract_text_from_pdf(path)
            if text:
                documents[filename] = text
                tokens = preprocess.preprocess(text)
                for word in tokens:
                    inverted_index[word][filename] += 1
        else:
            print(f"Skipping {filename} (because it is not a PDF)")

    # Convert defaultdict to regular dicts before pickling. Pickle uses core objects only.
    inverted_index = {k: dict(v) for k, v in inverted_index.items()}

    with open(config.INDEX_PATH, "wb") as f:
        pickle.dump((inverted_index, documents), f)

    print(f"Indexing complete. {len(documents)} documents indexed.")
    print(f"Index saved at: {config.INDEX_PATH}")


if __name__ == "__main__":
    index_documents()
