from flask import Flask, request, Response, jsonify
from configuration import AdminConfiguration
from models import adminDb, Participant, Election, ElectionParticipant, Vote
from flask_jwt_extended import JWTManager, jwt_required
from roleCheck import roleCheck
from utils import checkEmptyCreateParticipant, checkEmptyCreateElection, checkDateTime, checkParticipants, \
    jsonifyParticipants, verifyElection, getResultsOfParliamentElection, getResultsOfPresidentElection
from dateutil import parser

# ---------------------------- PORT 5001 -------------------------------------- #

adminApp = Flask(__name__)
adminApp.config.from_object(AdminConfiguration)
jwt = JWTManager(adminApp)

@adminApp.route("/createParticipant", methods=["POST"])
@roleCheck(role="administrator")
def createParticipant():
    data = {
        "name": request.json.get("name", ""),
        "individual": request.json.get("individual", "")
    }
    msg = checkEmptyCreateParticipant(data)
    if msg != "OK":
        return jsonify(message=msg), 400
    # convert individual to boolean ???
    participant = Participant(name=data["name"], individual=data["individual"])
    adminDb.session.add(participant)
    adminDb.session.commit()
    id = participant.id
    return jsonify(id=id), 200

@adminApp.route("/getParticipants", methods=["GET"])
@roleCheck(role="administrator")
def getParticipants():
    participants = []
    for participant in Participant.query.all():
        participantData = {
            "id" : participant.id,
            "name" : participant.name,
            "individual" : participant.individual
        }
        participants.append(participantData)
    return jsonify(participants=participants), 200

@adminApp.route("/createElection", methods=["POST"])
@roleCheck(role="administrator")
def createElection():
    data = {
        "start": request.json.get("start", ""),
        "end": request.json.get("end", ""),
        "individual": request.json.get("individual", ""),
        "participants": request.json.get("participants", "")
    }
    msg = checkEmptyCreateElection(data)
    if msg != "OK":
        return jsonify(message=msg), 400
    msg = checkDateTime(data["start"], data["end"])
    if msg != "OK":
        return jsonify(message=msg), 400
    msg = checkParticipants(data["participants"], data["individual"])
    if msg != "OK":
        return jsonify(message=msg), 400
    startTime = parser.parse(str(data["start"]))
    endTime = parser.parse(str(data["end"]))
    election = Election(start=startTime, end=endTime, individual=data["individual"])
    adminDb.session.add(election)
    adminDb.session.commit()

    # creating poll numbers
    pollNumbers = []
    pollNumber = AdminConfiguration.STARTING_POLL_NUMBER
    for id in data["participants"]:
        bond = ElectionParticipant(participantId=id, electionId=election.id, pollNumber=pollNumber)
        adminDb.session.add(bond)
        adminDb.session.commit()
        pollNumbers.append(pollNumber)
        pollNumber += 1

    return jsonify(pollNumbers=pollNumbers), 200


@adminApp.route("/getElections", methods=["GET"])
@roleCheck(role="administrator")
def getElections():
    elections = []
    for election in Election.query.all():
        # print(election.participants)
        electionData = {
            "id": election.id,
            "start": str(election.start),
            "end": str(election.end),
            "individual": election.individual,
            "participants": jsonifyParticipants(election.participants)
        }
        elections.append(electionData)

    return jsonify(elections=elections), 200

@adminApp.route("/getResults", methods=["GET"])
@roleCheck(role="administrator")
def getResults():
    electionId = request.args.get("id", -1)
    if electionId == -1:
        return jsonify(message="Field id is missing."), 400
    msg = verifyElection(electionId)
    if msg != "OK":
        return jsonify(message=msg), 400
    election = Election.query.filter(Election.id == electionId).first()
    if election.individual:
        result = getResultsOfPresidentElection(election)
    else:
        result = getResultsOfParliamentElection(election)
    return jsonify(participants=result[0], invalidVotes=result[1]), 200

@adminApp.route("/", methods=["GET", "POST"])
def adminHomePage():
    return AdminConfiguration.homeText

if(__name__ == "__main__"):
    adminDb.init_app(adminApp)
    adminApp.run(debug=True, host="0.0.0.0", port=5001)