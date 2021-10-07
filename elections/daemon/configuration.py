import os

url = ""#os.environ["DATABASE_URL"]

sqlalchemyUrlDevelopment = "mysql+pymysql://root:root@localhost:3307/electionsDB"
sqlalchemyUrlDeployment = f"mysql+pymysql://root:root@{url}/electionsDB"

redisHostDevelopment = "localhost"
redisHostDeployment = ""#os.environ["REDIS_URI"]

class DaemonConfiguration:
    SQLALCHEMY_DATABASE_URI = sqlalchemyUrlDevelopment
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    REDIS_HOST = redisHostDevelopment
    REDIS_LIST_NAME = "pendingVotes"
    START_SENDING = "START"
    END_SENDING = "END"