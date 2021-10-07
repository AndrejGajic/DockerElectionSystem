from datetime import timedelta
import os

url = "" #os.environ["DATABASE_URL"]
sqlalchemyUrlDevelopment = "mysql+pymysql://root:root@localhost/authenticationDB"
sqlalchemyUrlDeployment = f"mysql+pymysql://root:root@{url}/authenticationDB"
secretKey = "JWT_SECRET_KEY"

adminData = {
    "jmbg" : "0000000000000",
    "email" : "admin@admin.com",
    "password" : "1",
    "forename" : "admin",
    "surname" : "admin"
}

class AuthConfiguration:
    SQLALCHEMY_DATABASE_URI = sqlalchemyUrlDevelopment
    JWT_SECRET_KEY = "JWT_SECRET_KEY"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JMBG_CHARACTERS = 13
    MAX_CHARACTERS = 256
    homeText = "<h2>Authentication home page.</h2><br><br>"\
                "<h3>Available functionalities:</h3><br>"\
                "/register - registration of new user. [POST]<br>"\
                "/login - logging in to the application. [POST]<br>"\
                "/refresh - refreshing access token. [POST]<br>"\
                "/delete - erasing user from database [administrators only] [POST]<br>"\
                "/check - checking if your access token is valid. [POST]<br>"\
                "/ - authentication home page. [GET/POST]"
