from flask import Flask, jsonify
import requests

app = Flask(__name__)


@app.route("/")
def hello():
    return jsonify({"status": "api online"})


@app.route("/iso_data/<iso>", methods=["GET"])
def iso_data(iso):
    vaccination_url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.json"
    try:

        vaccinations = requests.get(vaccination_url)
    except:
        return "False"
    vaccinations_dict = {}
    for item in vaccinations.json():
        if item["iso_code"]:
            vaccinations_dict[item["iso_code"]] = {
                "data": item["data"][-1],
                "iso_code": item["iso_code"].replace("OWID_", " "),
                "country": item["country"],
            }
    if iso in vaccinations_dict:
        return jsonify(vaccinations_dict[iso])


if __name__ == "__main__":
    app.run(host="0.0.0.0")
