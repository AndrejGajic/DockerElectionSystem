from flask import Flask, request, Response, jsonify
from configuration import ModConfiguration
from models import adminDb, Participant, Election, ElectionParticipant, Vote
from flask_jwt_extended import JWTManager, jwt_required
from roleCheck import roleCheck
from sqlalchemy import and_

# ---------------------------- PORT 5004 -------------------------------------- #

modApp = Flask(__name__)
modApp.config.from_object(ModConfiguration)
# jwt = JWTManager(modApp)


@modApp.route("/getParticipants", methods=["GET"])
def getParticipants():
    electionId = request.args.get("electionId", "")
    name = request.args.get("name", "")
    participants = []
    if electionId == "" and name == "":
        participants = Participant.query.all()
    elif electionId == "":
        participants = Participant.query.filter(
            Participant.name.ilike("%"+name+"%")
        ).all()
    elif name == "":
        participants = Participant.query.join(ElectionParticipant).filter(
            ElectionParticipant.electionId == electionId
        ).all()
    else:
        participants = Participant.query.join(ElectionParticipant).filter(
            and_(
                Participant.name.ilike("%"+name+"%"),
                ElectionParticipant.electionId == electionId
            )
        ).all()
    retObject = []
    for participant in participants:
        participantData = {
            "id": participant.id,
            "name": participant.name,
            "individual": participant.individual
        }
        retObject.append(participantData)

    return jsonify(participants=retObject), 200



@modApp.route("/", methods=["GET", "POST"])
def index():
    return "Modification home page."

if(__name__ == "__main__"):
    adminDb.init_app(modApp)
    modApp.run(debug=True, host="0.0.0.0", port=5004)