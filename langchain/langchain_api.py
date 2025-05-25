from flask import Flask, request, jsonify
from backend import process_question

app = Flask(__name__)

@app.route("/ask_question", methods=["POST"])
def ask_question():
    data = request.get_json()
    question = data.get("question")
    use_wikidata = data.get("use_wikidata", True)
    use_dbpedia = data.get("use_dbpedia", True)

    if question:
        response = process_question(question, use_wikidata, use_dbpedia)
        return jsonify({"answer": response})
    else:
        return jsonify({"error": "No se ha proporcionado una pregunta"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
