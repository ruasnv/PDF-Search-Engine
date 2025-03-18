from flask import Flask, request, jsonify, render_template
import IR_engine

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # Load search page

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    search_results = IR_engine.boolean_search(query)

    return render_template(
        "results.html",
        query=query,
        results=search_results["results"],
        search_time=search_results["search_time"],
        stemming_time=search_results["stemming_time"],
        total_time=search_results["total_time"]
    )

if __name__ == "__main__":
    app.run(debug=True)
