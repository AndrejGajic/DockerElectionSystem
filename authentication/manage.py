from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from configuration import AuthConfiguration
from models import authDb
from flask_script import Manager
from sqlalchemy_utils import create_database, database_exists

authManageApp = Flask(__name__)
authManageApp.config.from_object(AuthConfiguration)

authMigrate = Migrate(authManageApp, authDb)

authManager = Manager(authManageApp)
authManager.add_command("db", MigrateCommand)


if(__name__ == "__main__"):
    authDb.init_app(authManageApp)
    if not database_exists(AuthConfiguration.SQLALCHEMY_DATABASE_URI):
        create_database(AuthConfiguration.SQLALCHEMY_DATABASE_URI)
    authManager.run()
