from flask import Flask, request, Response, jsonify
from configuration import UserConfiguration
from roleCheck import roleCheck
from flask_jwt_extended import jwt_required, JWTManager, get_jwt
from csvParser import parse
from redis import Redis
from datetime import datetime
from dateutil import parser

# ---------------------------- PORT 5002 -------------------------------------- #

userApp = Flask(__name__)
userApp.config.from_object(UserConfiguration)
jwt = JWTManager(userApp)

@userApp.route("/vote", methods=["POST"])
@roleCheck(role="zvanicnik")
def vote():
    if not request.files:
        return jsonify(message="Field file is missing."), 400
    csvFile = request.files.get("file")
    if not csvFile:
        return jsonify(message="Field file missing."), 400
    data = parse(csvFile)
    if len(data) == 2 and str(data[0]) == "error":
        return jsonify(message=data[1]), 400
    # votes are ready to send on redis server
    userData = get_jwt()
    jmbg = userData["jmbg"]
    # sending votes on redis server
    print("Connecting...")
    with Redis(host=UserConfiguration.REDIS_HOST) as redis:
        print("Connected to redis server.")
        for row in data:
            currentDateTime = parser.parse(str(datetime.now()))
            redisString = "{}#{}#{}#{}".format(jmbg, currentDateTime, row[0], row[1])
            redis.rpush(UserConfiguration.REDIS_LIST_NAME, redisString)
        # redis.rpush(UserConfiguration.REDIS_LIST_NAME, UserConfiguration.END_SENDING)


    return Response(status=200)

@userApp.route("/", methods=["GET", "POST"])
def index():
    return UserConfiguration.homeText

if __name__ == "__main__":
    userApp.run(debug=True, host="0.0.0.0", port=5002)
