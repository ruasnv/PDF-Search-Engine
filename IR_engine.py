import math
import os
import re
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import time
from collections import defaultdict
import requests
#import fitz

# Installing and launching Apache Tika Server
# CMD: java -jar tika-server.jar

# Extracting text from each file
# Replace the file_path with field of your choice
file_path = 'D:\\books'
documents = {}

#Alternative Method of extracting text with PyMuPDF - Faster, works only with PDFs, doesn't relay on HTTP requests,
'''
def extract_text(file_path):
    with fitz.open(file_path) as doc:
        return "\n".join(page.get_text() for page in doc)
'''

#Extract text and metadata from PDFs using Tika
def extract_text(file_path):
    tika_url = "http://localhost:9998/tika"
    with open(file_path, "rb") as f:
        response = requests.put(tika_url, data=f)
        return response.text

# Read all files from folder and extract text
for filename in os.listdir(file_path):
    file_full_path = os.path.join(file_path, filename)
    try:
        extracted_text = extract_text(file_full_path)
        documents[filename] = extracted_text
    except Exception as e:
        print(f"Error extracting {filename}: {e}")


# Preprocessing Steps
stemmer = PorterStemmer()

# Tokenizing and Cleaning = Removes punctuations, stopwords and lowercase everything.
def preprocess(text):
    """Tokenize, remove punctuations, apply stemming"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text) # Remove punctuation
    tokens = word_tokenize(text) #Tokenize text
    stemming_applied_tokens = [stemmer.stem(word) for word in tokens] #Apply stemming to each token
    return stemming_applied_tokens

# Indexing
# Inverted Index Creation
# Each word maps to the file that contains it.
inverted_index = defaultdict(lambda : defaultdict(int)) # a dictionary that has a dictionary inside mapped to a integer

def index_documents(doc_folder):
    """Indexes all documents in a folder, stores words and frequencies per document."""
    global documents
    documents = {}

    for filename in os.listdir(doc_folder):
        if filename.endswith(".pdf"):
            file_path = os.path.join(doc_folder, filename)
            text = extract_text(file_path)
            documents[filename] = text #Stores the full text

        words = preprocess(text)
        for word in words:
            inverted_index[word][filename] += 1 #For each occurrence, increase frequency by one!


index_documents(file_path)


# Searching
# Boolean Search - Can use Logic Operators in queries (AND, OR, NOT) sort by frequency, and return a context snippet
def boolean_search(query, window_size=50):
    start_time = time.time()  # Start timing for performance measure, so we can see how long it takes to seach

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