from flask import Flask
from configuration import AdminConfiguration
from models import adminDb
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from sqlalchemy_utils import create_database, database_exists

adminManageApp = Flask(__name__)
adminManageApp.config.from_object(AdminConfiguration)

adminMigrate = Migrate(adminManageApp, adminDb)
manager = Manager(adminManageApp)
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    adminDb.init_app(adminManageApp)
    if not database_exists(AdminConfiguration.SQLALCHEMY_DATABASE_URI):
        create_database(AdminConfiguration.SQLALCHEMY_DATABASE_URI)
    # adminManageApp().run()
    manager.run()