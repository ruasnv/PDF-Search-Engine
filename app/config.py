import os

from dotenv import load_dotenv

load_dotenv()

#the directory where config.py lives
APP_DIR = os.path.dirname(os.path.abspath(__file__))

#project root
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, ".."))

# Paths
DOCS_PICKLE = os.path.join(PROJECT_ROOT, "data", "docs.pkl")
INDEX_PICKLE = os.path.join(PROJECT_ROOT, "data", "index.pkl")
TFIDF_PICKLE = os.path.join(PROJECT_ROOT, "data", "tfidf.pkl")
DF_PICKLE = os.path.join(PROJECT_ROOT, "data","df.pkl")
DOC_LENGTHS_PICKLE = os.path.join(PROJECT_ROOT,"data","doc_length.pkl")
TERMS_PICKLE = os.path.join(PROJECT_ROOT,"data","terms.pkl")
PREPROCESSED_TERMS_PICKLE = os.path.join(PROJECT_ROOT,"data","preprocessed_terms.pkl")
DOCS_PATH = os.getenv("DOCS_FOLDER")