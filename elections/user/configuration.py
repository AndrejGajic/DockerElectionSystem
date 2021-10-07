import os

redisHostDevelopment = "localhost"
redisHostDeployment = ""#os.environ["REDIS_URI"]

class UserConfiguration:
    # SQLALCHEMY_DATA_URI = sqlalchemyUrlDevelopment
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    REDIS_HOST = redisHostDevelopment
    REDIS_LIST_NAME = "pendingVotes"
    START_SENDING = "START"
    END_SENDING = "END"
    homeText = "<h2>Officials home page.</h2><br><br>" \
               "<h3>Available functionalities [officials only]:</h3><br>" \
               "/vote - sending list of votes (.csv file) to redis server. [POST]<br>" \
               "/ - officials home page. [GET/POST]"