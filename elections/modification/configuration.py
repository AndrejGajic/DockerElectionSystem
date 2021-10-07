import os

url = ""#os.environ["DATABASE_URL"]
sqlalchemyUrlDevelopment = "mysql+pymysql://root:root@localhost:3307/electionsDB"
sqlalchemyUrlDeployment = f"mysql+pymysql://root:root@{url}/electionsDB"

class ModConfiguration:
    SQLALCHEMY_DATABASE_URI = sqlalchemyUrlDevelopment
    JWT_SECRET_KEY = "JWT_SECRET_KEY"