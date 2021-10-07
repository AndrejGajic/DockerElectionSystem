from flask import Flask
from configuration import AdminConfiguration
from flask_migrate import Migrate, init, migrate, upgrade
from models import adminDb
from sqlalchemy_utils import create_database, database_exists

electionMigrateApp = Flask(__name__)
electionMigrateApp.config.from_object(AdminConfiguration)

electionMigrateObject = Migrate(electionMigrateApp, adminDb)

done = False
while not done:
    try:
        if not database_exists(electionMigrateApp.config["SQLALCHEMY_DATABASE_URI"]):
            create_database(electionMigrateApp.config["SQLALCHEMY_DATABASE_URI"])
        adminDb.init_app(electionMigrateApp)

        with electionMigrateApp.app_context() as context:
            init()
            migrate(message="Production migration.")
            upgrade()
            done = True
        # filling database with data at some point of project ?

    except Exception as exception:
        print(exception)