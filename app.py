from flask import Flask, jsonify, make_response
import requests

app = Flask(__name__)
vaccination_url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.json"


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/get_iso_data/<iso>", methods=["GET"])
def update_iso_data(iso):
    # Takes iso_code: ISO 3166-1 alpha-3 – three-letter country codes and returns latest vaccination rates.
    # USA
    # OWID_WRL

    try:
        vaccinations = requests.get(vaccination_url)
    except:
        return "False"
    vaccinations_dict = {}
    for item in vaccinations.json():
        if item["iso_code"]:
            vaccinations_dict[item["iso_code"]] = {
                "data": item["data"][-1],
                "country": item["country"],
            }
    if iso in vaccinations_dict:
        response = make_response(jsonify(vaccinations_dict[iso]), 200)
        return response
    else:
        response = make_response(jsonify({"error": "No data for this country"}), 404)


if __name__ == "__main__":
    app.run(debug=True)
