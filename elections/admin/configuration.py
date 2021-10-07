import os

url = ""#os.environ["DATABASE_URL"]
sqlalchemyUrlDevelopment = "mysql+pymysql://root:root@localhost:3307/electionsDB"
sqlalchemyUrlDeployment = f"mysql+pymysql://root:root@{url}/electionsDB"

class AdminConfiguration:
    SQLALCHEMY_DATABASE_URI = sqlalchemyUrlDevelopment
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    STARTING_POLL_NUMBER = 1
    ELECTION_ROUNDS = 250
    ELECTION_TRESHOLD = 0.05
    homeText = "<h2>Admin home page.</h2><br><br>" \
               "<h3>Available functionalities [administrators only]:</h3><br>" \
               "/createParticipant - create new participant in elections (individual or political party). [POST]<br>" \
               "/getParticipants - returns list of all participants. [GET]<br>" \
               "/createElection - creating new election. [POST]<br>" \
               "/getElections - returns list of all elections. [GET]<br>" \
               "/getResults?<electionId> - returns result of certain election (if not active). [GET]<br>" \
               "/ - admin home page. [GET/POST]"
    testsConfiguration = "--authentication-address http://127.0.0.1:5000 --jwt-secret JWT_SECRET_KEY --user-role zvanicnik --administrator-role administrator --administrator-address http://127.0.0.1:5001 --with-authentication --station-address http://127.0.0.1:5002 --roles-field role --type all"