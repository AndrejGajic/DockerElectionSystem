from flask_sqlalchemy import SQLAlchemy
from configuration import AuthConfiguration

authDb = SQLAlchemy()

class User(authDb.Model):
    __tablename__ = "users"
    id = authDb.Column(authDb.Integer, primary_key=True)
    jmbg = authDb.Column(authDb.String(256), nullable=False)
    forename = authDb.Column(authDb.String(256), nullable=False)
    surname = authDb.Column(authDb.String(256), nullable=False)
    email = authDb.Column(authDb.String(256), nullable=False)
    password = authDb.Column(authDb.String(256), nullable=False)

    roleId = authDb.Column(authDb.Integer, authDb.ForeignKey("roles.id"), nullable=False)
    role = authDb.relationship("Role", back_populates="users")

    def __repr__(self):
        return f"{self.forename} {self.surname} {self.email} #{self.jmbg}"

class Role(authDb.Model):
    __tablename__ = "roles"
    id = authDb.Column(authDb.Integer, primary_key=True)
    name = authDb.Column(authDb.String(256), nullable=False)

    users = authDb.relationship("User", back_populates="role")

    def __repr__(self):
        return self.name
