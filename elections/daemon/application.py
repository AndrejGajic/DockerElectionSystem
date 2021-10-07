from flask import Flask
from redis import Redis
from configuration import DaemonConfiguration
from models import adminDb, Vote, Election
from utils import checkValidity

daemonApp = Flask(__name__)
daemonApp.config.from_object(DaemonConfiguration)
adminDb.init_app(daemonApp)  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# def runDaemon():

while True:
    try:
        with daemonApp.app_context() as context:
            print("Connecting...")
            with Redis(host=DaemonConfiguration.REDIS_HOST) as redis:
                print("Connected.")
                while True:
                    list = redis.lrange(DaemonConfiguration.REDIS_LIST_NAME, 0, -1)
                    if len(list) > 0:
                        bytes = redis.lpop(DaemonConfiguration.REDIS_LIST_NAME)
                        content = bytes.decode("utf-8")
                        voteData = content.split("#")
                        if len(voteData) != 4:
                            print("Invalid data!")
                            continue
                        data = {
                            "voterJmbg": voteData[0],
                            "voteDateTime": voteData[1],
                            "guid": voteData[2],
                            "pollNumber": voteData[3]
                        }
                        msg = checkValidity(data)
                        if msg == "Invalid vote":  # no active elections!
                            print("Invalid vote : There are no active elections.")
                            # print(data["voteDateTime"])
                            continue
                        msgContent = msg.split("#")
                        if len(msgContent) != 2:
                            print("Unexpected error.")
                            continue
                        msg = msgContent[0]
                        electionId = int(msgContent[1])
                        if msg == "Duplicate ballot":  # duplicate ballot on active election
                            print("Invalid vote : Duplicate ballot.")
                            vote = Vote(guid=data["guid"], electionId=electionId, jmbg=data["voterJmbg"],
                                        pollNumber=data["pollNumber"], valid=False, invalidReason="Duplicate ballot.")
                            print(vote.print())
                            adminDb.session.add(vote)
                            adminDb.session.commit()
                        elif msg == "Invalid poll number":  # there is no participants with pollNumber on active election
                            print("Invalid vote : Invalid poll number.")
                            vote = Vote(guid=data["guid"], electionId=electionId, jmbg=data["voterJmbg"],
                                        pollNumber=data["pollNumber"], valid=False, invalidReason="Invalid poll number.")
                            print(vote.print())
                            adminDb.session.add(vote)
                            adminDb.session.commit()
                        elif msg == "OK":
                            vote = Vote(guid=data["guid"], electionId=electionId, jmbg=data["voterJmbg"],
                                        pollNumber=data["pollNumber"], valid=True)
                            # print(vote.print())
                            adminDb.session.add(vote)
                            adminDb.session.commit()
                            # print("Valid vote.")
                        else:
                            print("Unexpected error.")
    except Exception as exception:
        print(exception)




# with daemonApp.app_context() as context:
#    runDaemon()
