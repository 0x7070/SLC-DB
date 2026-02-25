from flask import Flask, render_template, request, redirect, jsonify
import database, os, json

app = Flask(__name__)
database.init_db()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLACEHOLDERS_PATH = os.path.join(BASE_DIR, "placeholders.json")

with open(PLACEHOLDERS_PATH) as f:
    placeholders = json.load(f)


@app.route("/")
def index():
    films = database.get_all_films()
    return render_template("index.html", films=films)


@app.route("/add", methods=["GET", "POST"])
def add():
    form_data = {}
    duplicate = None
    error = None

    if request.method == "POST":
        form_data = request.form.to_dict()
        barcode = form_data.get("barcode", "")
        name = form_data.get("name", "")
        brand = form_data.get("brand", "")
        film_type = form_data.get("film_type", "")
        weight = form_data.get("weight", "")
        notes = form_data.get("notes", "")

        success, duplicate = database.insert_film(barcode, name, brand, film_type, weight, notes)

        if success:
            return redirect("/")
        else:
            error = "Duplicate barcode detected"

    return render_template(
        "add.html",
        placeholders=placeholders,
        form_data=form_data,
        duplicate=duplicate,
        error=error
    )


@app.route("/search")
def search():
    term = request.args.get("q", "").lower()
    films = database.get_all_films()
    filtered = [f for f in films if
                term in str(f["barcode"]).lower() or
                term in str(f["name"]).lower() or
                term in str(f["brand"]).lower() or
                term in str(f["film_type"]).lower() or
                term in str(f["notes"]).lower()]
    return jsonify([dict(f) for f in filtered])


if __name__ == "__main__":
    app.run(debug=True)