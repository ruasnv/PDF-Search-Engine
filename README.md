PDF Search Engine
=================

Goal of the Project
-------------------

This project aims to implement a simple and efficient search engine for PDF documents stored on your local machine. The goal is to provide full-text search functionality using custom indexing methods, allowing users to search through PDF documents based on content.

**Note**: We did not use Lucene for this project. Instead, we've implemented a lightweight search system from scratch.

Features
--------

*   **Search Method**: We use a basic **inverted index** approach to map terms to the documents they appear in. This allows for quick lookups of documents based on search queries.
    
*   **Indexing Method**: The indexing process extracts and processes the text from PDF files using PyMuPDF (formerly known as fitz) and stores it in an inverted index structure.
    
*   **Stemming**: We use the **Porter Stemmer** algorithm to reduce words to their root form, improving search results by matching different word variants.
    

Repository Structure and Running the App
----------------------------------------

The repository is structured as follows:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   /app      /data             # Directory for storing the index files      /templates        # HTML templates for the Flask web interface      /static           # Static files (e.g., CSS, JS)      app.py            # Main Flask app file      indexer.py        # Indexing script      searcher.py       # Search logic      requirements.txt  # List of required dependencies      Dockerfile        # Dockerfile for containerization   `

### Running the Application

1.  python -m venv .venv.\\.venv\\Scripts\\activate
    
2.  pip install -r requirements.txt
    
3.  python app.py
    
4.  The app will be available at [http://localhost:5000](http://localhost:5000).
    

### Docker

The project is Dockerized for easy deployment. To run the project using Docker, follow these steps:

1.  docker build -t pdf-search .
    
2.  docker run -p 5000:5000 pdf-search
    

The app will be accessible at [http://localhost:5000](http://localhost:5000) from within the Docker container.

Performance and Limitations
---------------------------

*   **Performance**: The search speed is decent for small to medium-sized document sets. As the number of documents increases, performance may degrade as the indexing size grows.
    
*   **Limitations**: This search engine currently only supports PDFs. It does not index metadata or perform advanced features like TF-IDF scoring or caching, but these are planned for future improvements.
    

Future Improvements
-------------------

*   **TF-IDF Scoring**: Implementing Term Frequency-Inverse Document Frequency (TF-IDF) scoring will improve search relevance by weighting terms based on their frequency in the document versus the entire dataset.
    
*   **Caching**: Implement caching to store the results of frequent searches and reduce search time for popular queries.
    
*   **Search by Metadata**: Integrating metadata extraction (e.g., author, title) using Tika would allow for richer search capabilities. Tika could be used to extract additional information from PDFs and other file formats beyond the raw text content.
    

How We Process Documents
------------------------

We use **PyMuPDF** (also known as **fitz**) to extract text from PDFs. PyMuPDF is chosen because:

*   **Speed**: It is faster than Java-based tools like Tika.
    
*   **Local Processing**: It works entirely locally without the need for external servers or services.
    
*   **PDF Focused**: Since the project focuses on extracting text from PDFs, PyMuPDF provides all the functionality we need without dealing with additional overhead from extracting metadata.
    

Why Not Use Tika?
-----------------

While Tika is great for extracting both text and metadata from various file formats, we chose to use **PyMuPDF** (fitz) for the following reasons:

*   **Speed**: PyMuPDF is much faster than Tika for processing PDFs.
    
*   **Local**: Tika requires a Java server to run, which adds complexity. PyMuPDF works entirely within the Python environment, making it easier to set up and run.
    
*   **Simplified Use Case**: Our use case only requires extracting text from PDF documents, and PyMuPDF is more than sufficient for this purpose. We don't need the extra functionality Tika provides for extracting metadata or processing other file types.
    

This project serves as a foundational search engine for PDFs. Feel free to extend it and add more advanced features as you see fit! 😊
