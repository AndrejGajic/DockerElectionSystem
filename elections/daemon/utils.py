from models import adminDb, Election, Vote, ElectionParticipant
from datetime import datetime
from dateutil import parser
from sqlalchemy import and_

def checkValidity(data):
    # 1 -> check if there is active election
    activeElection = None
    for election in Election.query.all():
        if election.start < parser.parse(data["voteDateTime"]) and election.end > parser.parse(data["voteDateTime"]):
            activeElection = election
            break  # there is maximum 1 active election at the time...

    if activeElection is None:
        return "Invalid vote"

    # 2 -> check if there is duplicate ballot
    for vote in Vote.query.all():
        if vote.guid == data["guid"]: # and vote.electionId == election.id:  # duplicate ballot -> same guid globally
            returnMsg = "{}#{}".format("Duplicate ballot", activeElection.id)
            # print(returnMsg)
            # print(data["guid"])
            return returnMsg

    # 3 -> check if there is participant with pollNumber on active election
    electionParticipant = ElectionParticipant.query.filter(
        and_(
            ElectionParticipant.electionId == activeElection.id,
            ElectionParticipant.pollNumber == data["pollNumber"]
        )
    ).first()
    if not electionParticipant:  # there is no participant with pollNumber on active election
        returnMsg = "{}#{}".format("Invalid poll number", activeElection.id)
        # print(returnMsg)
        # print(data["guid"])
        return returnMsg

    # Vote is valid and is ready for proccessing!
    returnMsg = "{}#{}".format("OK", activeElection.id)
    return returnMsg
