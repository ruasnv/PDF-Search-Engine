import math
import os
import re
import time
from collections import defaultdict
import requests

# Installing and launching Apache Tika Server
# CMD: java -jar tika-server.jar

# Extracting text from each file
# Replace the file_path with field of your choice
file_path = 'D:\\books'
documents = {}


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

#print("Test 1: ", extract_text("D:\\books\\time-clocks.pdf"))  # A test to see if everything is okay

# Preprocessing Steps
# Tokenizing and Cleaning = Removes punctuations, stopwords and lowercase everything.
def tokenize(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    return text.split()


#print("Tokenize function test: ",
     # tokenize("Tokenization FunCTIOn, seems to be working - well!"))  # ['hello', 'world', 'this', 'is', 'ir']

# Indexing
# Inverted Index Creation
# Each word maps to the file that contains it.
inverted_index = defaultdict(set)

for filename, text in documents.items():
    words = tokenize(text)
    for word in words:
        inverted_index[word].add(filename)


# Searching
# Booelan Search - Can use Logic Operators in queries (AND, OR, NOT)
def boolean_search(query):
    start_time = time.time()  # Start timing
    words = tokenize(query)  # Preprocessing

    stemming_start = time.time()
    stemmed_words = set(words)  # If you apply stemming
    stemming_time = time.time() - stemming_start

    search_start = time.time()
    results = []

    for filename, text in documents.items():
        text_tokens = tokenize(text)
        for word in stemmed_words:
            if word in text_tokens:
                # Get first occurrence index
                index = text_tokens.index(word)
                context_window = text_tokens[max(0, index - 10): index + 10]  # 10 words before & after
                snippet = " ".join(context_window).replace(word, f"**{word}**")  # Highlight word
                results.append((filename, snippet))
                break  # Stop after first match in a file

    search_time = time.time() - search_start
    total_time = time.time() - start_time

    return {
        "results": results,
        "search_time": round(search_time, 4),
        "stemming_time": round(stemming_time, 4),
        "total_time": round(total_time, 4)
    }


#print("Test for boolean search: What documents contain the words 'Transformers' are ", boolean_search("Transformers"))


# Ranking the results
# TF-IDF Scoring, ranks results based on the highest TF-IDF score
# Calculate Term Frequency
def tf(word, doc):
    return doc.count(word) / len(doc)


# Calculate Inverse Document Frequency
def idf(word, all_docs):
    doc_count = sum(1 for doc in all_docs if word in doc)
    return math.log(len(all_docs) / (1 + doc_count))


def tfidf(word, doc, all_docs):
    return tf(word, doc) * idf(word, all_docs)
