from flask import Flask, jsonify
import requests

app = Flask(__name__)

# Setup a health route to check if the service is up
@app.route("/")
@app.route("/health")
def hello():
    response = jsonify({"status": "api online"})
    response.status_code = 200
    return response


# Setup a GET route for requesting the data of the requested ISO Code.
@app.route("/iso_data/<iso>", methods=["GET"])
def iso_data(iso):
    # Get the OWID Data from GitHub
    vaccination_url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.json"
    try:
        vaccinations = requests.get(vaccination_url)
    except:
        return "False"

    vaccinations_dict = {}
    # Using lambda and filter to find our requested ISO Code
    item = list(filter(lambda x: x["iso_code"] == iso, vaccinations.json()))
    if item:
        item = item[0]
        # If data is found format it for our response.
        vaccinations_dict = {
            "data": item["data"][-1],
            "iso_code": item["iso_code"].replace("OWID_", " "),
            "country": item["country"],
        }
        response = jsonify(vaccinations_dict)
        # Returning a 203 since it's a mirror of the OWID data.
        response.status_code = 203
    else:
        # If no data is found return a 404.
        response = jsonify(
            {"status": 404, "error": "not found", "message": "invalid iso code URI"}
        )
        response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")
