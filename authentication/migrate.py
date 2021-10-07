from flask import Flask
from configuration import AuthConfiguration, adminData
from flask_migrate import Migrate, init, migrate, upgrade
from models import authDb, User, Role
from sqlalchemy_utils import create_database, database_exists

authMigrateApp = Flask(__name__)
authMigrateApp.config.from_object(AuthConfiguration)

authMigrateObject = Migrate(authMigrateApp, authDb)

done = False
while not done:
    try:
        if not database_exists(AuthConfiguration.SQLALCHEMY_DATABASE_URI):
            create_database(AuthConfiguration.SQLALCHEMY_DATABASE_URI)
        authDb.init_app(authMigrateApp)

        with authMigrateApp.app_context() as context:
             init()
             migrate(message="Production migration.")
             upgrade()

             # database initialization

             adminRole = Role(name="administrator")
             userRole = Role(name="zvanicnik")

             authDb.session.add(adminRole)
             authDb.session.add(userRole)
             authDb.session.commit()

             administrator = User(
                 jmbg = adminData["jmbg"],
                 email = adminData["email"],
                 password = adminData["password"],
                 forename = adminData["forename"],
                 surname = adminData["surname"],
                 roleId = adminRole.id
             )
             authDb.session.add(administrator)
             authDb.session.commit()


             done = True
    except Exception as exception:
        print(exception)