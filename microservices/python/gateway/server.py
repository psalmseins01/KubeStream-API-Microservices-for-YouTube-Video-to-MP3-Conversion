import os, gridfs, pika, json # type: ignore
from flask import Flask, request, send_file, jsonify
from flask_pymongo import PyMongo # type: ignore
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId

app = Flask(__name__)

mongo_video = PyMongo(
    app,
    uri="mongodb://host.minikube.internal:27017/videos"
)

mongo_mp3 = PyMongo(
    app,
    uri="mongodb://host.minikube.internal:27017/mp3s"
)

fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

@app.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)
    if err is None:
        return token
    else:
        return err

@app.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)
    if err:
        return jsonify({"message": err})

    access = json.loads(access)

    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return jsonify({"message": "exactly 1 file required"}), 400
        
        for _, f in request.files.items():
            err = util.upload(f, fs_videos, channel, access)

            if err:
                return jsonify({"message": err})
        return jsonify({"Success"}), 200
    else:
        return jsonify({"message": "Not authorized"}), 401
    
@app.route("/download", methods=["GET"])
def download():
    access, err = validate.token(request)
    if err:
        return jsonify({"message": err})

    access = json.loads(access)

    if access["admin"]:
        fid_str = request.args.get("fid")
        if fid_str is None:
            return jsonify({"message": "fid is required"}), 400
        try:
            out = fs_mp3s.get(ObjectId(fid_str))
            return send_file(out, download_name=f'{fid_str}.mp3')
        except Exception as e:
            print(e.__str__)
            return json({"message": "internal server error"}), 500

    return jsonify({"message": "not authorized"}), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

