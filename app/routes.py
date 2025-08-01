from flask import request, jsonify
from flask_cors import cross_origin
import json


def register_routes(app):
    @app.route("/autofocus/", methods=["POST"])
    @cross_origin()
    def autofocus():
        app.cam.AutoFocus()
        return jsonify({"message": "AutoFocus triggered"})

    @app.route("/command/", methods=["POST"])
    @cross_origin()
    def command():
        data = request.get_json()
        result = app.cam.Command(data.get("cgi"), json.loads(data.get("params", "{}")))
        return jsonify({"message": "ok", "result": result})

    @app.route("/set-color-mode/", methods=["POST"])
    @cross_origin()
    def set_color_mode():
        data = request.get_json()
        result = app.cam.SetColorMode(color_mode_code=data.get("color_mode",1))
        return jsonify({"message": "ok", "result": result})
