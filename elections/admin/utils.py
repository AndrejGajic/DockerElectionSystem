from datetime import datetime
from dateutil import parser
from models import Election, Participant, Vote, ElectionParticipant
from configuration import AdminConfiguration
from sqlalchemy import and_


def checkEmptyCreateParticipant(data):
    if data["name"] == "":
        return "Field name is missing."
    elif data["individual"] == "":
        return "Field individual is missing."
    else:
        return "OK"

def checkEmptyCreateElection(data):
    if data["start"] == "":
        return "Field start is missing."
    elif data["end"] == "":
        return "Field end is missing."
    elif data["individual"] == "":
        return "Field individual is missing."
    elif data["participants"] == "":
        return "Field participants is missing."
    else:
        return "OK"

def checkDateTime(start, end):
    msg = "Invalid date and time."
    # format check
    try:
        startDT = parser.parse(start)
        endDT = parser.parse(end)
    except ValueError:
        return msg
    if start > end:
        return msg
    # overlapping check
    elections = Election.query.all()
    for election in elections:
        startDT2 = parser.parse(str(election.start))
        endDT2 = parser.parse(str(election.end))
        if not ((startDT < startDT2 and endDT < startDT2) or (startDT > startDT2 and startDT > endDT2)):
            return msg
    return "OK"

def checkParticipants(participants, individual):
    msg = "Invalid participants."
    if participants == "" or len(participants) < 2:
        return msg
    for id in participants:
        participant = Participant.query.filter(Participant.id == id).first()
        if not participant or participant.individual != individual:
            return msg
    return "OK"

def jsonifyParticipants(participants):
    jsonifiedParticipants = []
    for participant in participants:
        # participant = Participant.query.filter(Participant.id == id).first()
        participantData = {
            "id": participant.id,
            "name": participant.name
        }
        jsonifiedParticipants.append(participantData)
    return jsonifiedParticipants

def verifyElection(electionId):
    election = Election.query.filter(Election.id == electionId).first()
    if not election:
        return "Election does not exist."
    elif parser.parse(str(datetime.now())) < election.end:
        return "Election is ongoing."
    else:
        return "OK"


def getResultsOfPresidentElection(election):
    votes = Vote.query.filter(Vote.electionId == election.id).all()
    votesPerParticipant = []
    totalValidVotes = 0
    for participant in election.participants:
        votesPerParticipant.append(0)
    print(len(votesPerParticipant))
    participants = []
    invalidVotes = []
    for vote in votes:
        if not vote.valid:
            invalidVote = {
                "electionOfficialJmbg": vote.jmbg,
                "ballotGuid": vote.guid,
                "pollNumber": vote.pollNumber,
                "reason": vote.invalidReason
            }
            invalidVotes.append(invalidVote)
        else:
            votesPerParticipant[vote.pollNumber - 1] += 1
            totalValidVotes += 1

    index = 1
    for participant in election.participants:
        if totalValidVotes == 0:
            result = 0
        else:
            result = round(votesPerParticipant[index - 1] / totalValidVotes, 2)
        participantObject = {
            "pollNumber": index,
            "name": participant.name,
            "result": result
        }
        index += 1
        participants.append(participantObject)

    retObject = []
    retObject.append(participants)
    retObject.append(invalidVotes)
    return retObject

def getResultsOfParliamentElection(election):
    validVotes = Vote.query.filter(
        and_(
            Vote.electionId == election.id,
            Vote.valid == 1
        )
    ).all()
    totalValidVotes = len(validVotes)
    # poll number is ORDINAL number of participants in election!
    votesPerParticipant = []
    for participant in election.participants:
        votesPerParticipant.append(0)
    # counting total votes per party
    for vote in validVotes:
        votesPerParticipant[vote.pollNumber - 1] += 1
    rounds = AdminConfiguration.ELECTION_ROUNDS
    threshold = AdminConfiguration.ELECTION_TRESHOLD
    passedParties = []
    eliminatedParties = []
    # eliminating parties which did not passed the threshold
    index = 1
    for votes in votesPerParticipant:
        if totalValidVotes > 0 and (votes / totalValidVotes) >= threshold:
            party = {
                "participant": election.participants[index - 1],
                "votes": votes,
                "result": 0,
                "pollNumber": index
            }
            passedParties.append(party)
        else:
            eliminatedParty = {
                "participant": election.participants[index - 1],
                "pollNumber": index
            }
            eliminatedParties.append(eliminatedParty)
        index += 1
    # election process -> D'Hondt method (quot = V / (s + 1) ; V -> total number of votes; s-> current score of party)
    if len(passedParties) > 0:
        while rounds > 0:
            winnerIndex = 0
            index = 0
            maxQuot = 0
            for party in passedParties:
                quot = float(party["votes"]) / (party["result"] + 1)
                if quot > maxQuot:
                    maxQuot = quot
                    winnerIndex = index
                index += 1
            passedParties[winnerIndex]["result"] += 1
            rounds -= 1
    # creating output arrays
    retObject = []
    # creating output array of participants (with their results on the election)
    participantsRet = []
    for party in passedParties:
        participantObject = {
            "pollNumber": party["pollNumber"],
            "name": party["participant"].name,
            "result": party["result"]
        }
        participantsRet.append(participantObject)
    for party in eliminatedParties:
        participantObject = {
            "pollNumber": party["pollNumber"],
            "name": party["participant"].name,
            "result": 0
        }
        participantsRet.append(participantObject)

    retObject.append(participantsRet)
    # creating output array of invalid votes
    invalidVotesRet = []
    invalidVotes = Vote.query.filter(
        and_(
           Vote.electionId == election.id,
           Vote.valid == 0
        )
    ).all()
    for vote in invalidVotes:
        invalidVote = {
            "electionOfficialJmbg": vote.jmbg,
            "ballotGuid": vote.guid,
            "pollNumber": vote.pollNumber,
            "reason": vote.invalidReason
        }
        invalidVotesRet.append(invalidVote)

    retObject.append(invalidVotesRet)
    return retObject