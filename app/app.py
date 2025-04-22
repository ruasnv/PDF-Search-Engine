from flask import Flask, request, render_template, redirect, url_for
import searcher
import indexer

app = Flask(__name__)

indexer.document_index()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    search_results = searcher.search(query)

    return render_template(
        "results.html",
        query=search_results["query"],
        results=search_results["results"],
        search_time=search_results["search_time"],
        total_time=search_results["total_time"],
    )


@app.route("/rebuild", methods=["POST"])
def rebuild():
    indexer.document_index()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
