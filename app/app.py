from flask import Flask, request, render_template, redirect, url_for
import searcher
import indexer
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # Load search page

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    search_results = searcher.boolean_search(query)

    return render_template(
        "/templates/results.html",
        query=query,
        results=search_results["results"],
        search_time=search_results["search_time"],
        stemming_time=search_results["stemming_time"],
        total_time=search_results["total_time"]
    )
@app.route("/rebuild", methods=["POST"])
def rebuild():
    indexer.index_documents()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
