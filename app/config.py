import os

#the directory where config.py lives
APP_DIR = os.path.dirname(os.path.abspath(__file__))

#project root
PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, ".."))

# Paths
INDEX_PATH = os.path.join(PROJECT_ROOT, "data", "index.pkl")
DOC_INDEX = os.path.join(PROJECT_ROOT, "data", "docs.pkl")
DOCS_PATH = "D:/books"