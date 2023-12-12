"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route("/")
def sitemap():
    return generate_sitemap(app)


@app.route("/members", methods=["GET"])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"family": members}

    return jsonify(response_body), 200


@app.route("/members/<member_id>", methods=["GET"])
def handle_get_one_member(member_id):
    member = jackson_family.get_member(member_id)

    if member is None:
        return jsonify({"error": "Member not found"}), 404

    return jsonify(member), 200


@app.route("/members", methods=["POST"])
def handle_add_member():
    json_data = request.get_json()
    required_keys = ["first_name", "age", "lucky_numbers"]
    for key in required_keys:
        if key not in json_data:
            return f"missing {key} key from the request body", 400

    if not isinstance(json_data["age"], int):
        return "age is not an integer", 400

    new_member = {
        "first_name": json_data["first_name"],
        "age": json_data["age"],
        "lucky_numbers": json_data["lucky_numbers"],
    }

    inner_member_data = jackson_family.add_member(new_member)
    return jsonify(inner_member_data), 201


# this only runs if `$ python src/app.py` is executed
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=True)
